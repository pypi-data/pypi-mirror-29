# Created: 13.03.2016, 2018 rewritten for pytest
# Copyright (C) 2016-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
import pytest

import ezdxf
from ezdxf.modern.image import ImageDef, Image
from ezdxf.lldxf.extendedtags import ExtendedTags


@pytest.fixture(scope='module')
def dwg():
    return ezdxf.new('AC1015')


@pytest.fixture(scope='module')
def image_def(dwg):
    tags = ExtendedTags.from_text(IMAGE_DEF)
    return ImageDef(tags, dwg)


def test_imagedef_attribs(image_def):
    assert 'IMAGEDEF' == image_def.dxftype()
    assert 0 == image_def.dxf.class_version
    assert 'mycat.jpg' == image_def.dxf.filename
    assert (640., 360.) == image_def.dxf.image_size
    assert (.01, .01) == image_def.dxf.pixel_size
    assert 1 == image_def.dxf.loaded
    assert 0 == image_def.dxf.resolution_units


@pytest.fixture(scope='module')
def image(dwg):
    tags = ExtendedTags.from_text(IMAGE)
    return Image(tags, dwg)


def test_image_dxf_attribs(image):
    assert 'IMAGE' == image.dxftype()
    assert (0., 0., 0.) == image.dxf.insert
    assert (.01, 0., 0.) == image.dxf.u_pixel
    assert (0., .01, 0.) == image.dxf.v_pixel
    assert (640., 360.) == image.dxf.image_size
    assert 7 == image.dxf.flags
    assert 0 == image.dxf.clipping
    assert 50 == image.dxf.brightness
    assert 50 == image.dxf.contrast
    assert 0 == image.dxf.fade
    assert 'DEAD' == image.dxf.image_def_reactor
    assert 1 == image.dxf.clipping_boundary_type
    assert 2 == image.dxf.count_boundary_points
    assert [(0, 0), image.dxf.image_size] == image.get_boundary_path()


def test_get_boundary_path(image):
    assert [(0, 0), (640, 360)] == image.get_boundary_path()


def test_reset_boundary_path(image):
    image.reset_boundary_path()
    assert 2 == image.dxf.count_boundary_points
    assert 3 == image.dxf.flags
    assert [(0, 0) == image.dxf.image_size], image.get_boundary_path()


def test_set_boundary_path(image):
    image.set_boundary_path([(0, 0), (640, 180), (320, 360)])  # 3 vertices triangle
    assert 3 == image.dxf.count_boundary_points
    assert 2 == image.dxf.clipping_boundary_type
    assert [(0, 0), (640, 180), (320, 360)], image.get_boundary_path()


@pytest.fixture
def new_dwg():
    return ezdxf.new('AC1015')


def test_new_image_def(new_dwg):
    rootdict = new_dwg.rootdict
    assert 'ACAD_IMAGE_DICT' not in rootdict
    imagedef = new_dwg.add_image_def('mycat.jpg', size_in_pixel=(640, 360))

    # check internals image_def_owner -> ACAD_IMAGE_DICT
    image_dict_handle = rootdict['ACAD_IMAGE_DICT']
    image_dict = new_dwg.get_dxf_entity(image_dict_handle)
    assert imagedef.dxf.owner == image_dict.dxf.handle

    assert 'mycat.jpg' == imagedef.dxf.filename
    assert (640., 360.) == imagedef.dxf.image_size

    # rest are default values
    assert (.01, .01) == imagedef.dxf.pixel_size
    assert 1 == imagedef.dxf.loaded
    assert 0 == imagedef.dxf.resolution_units


def test_create_and_delete_image(new_dwg):
    msp = new_dwg.modelspace()
    image_def = new_dwg.add_image_def('mycat.jpg', size_in_pixel=(640, 360))
    image = msp.add_image(image_def=image_def, insert=(0, 0), size_in_units=(3.2, 1.8))
    assert (0, 0, 0) == image.dxf.insert
    assert (0.005, 0, 0) == image.dxf.u_pixel
    assert (0., 0.005, 0) == image.dxf.v_pixel
    assert (640, 360) == image.dxf.image_size
    assert image_def.dxf.handle == image.dxf.image_def
    assert 3 == image.dxf.flags
    assert 0 == image.dxf.clipping
    assert 2 == image.dxf.count_boundary_points
    assert [(0, 0), image.dxf.image_size] == image.get_boundary_path()

    image_def2 = image.get_image_def()
    assert image_def.dxf.handle, image_def2.dxf.handle

    # does image def reactor exists
    reactor_handle = image.dxf.image_def_reactor
    assert reactor_handle in new_dwg.objects
    reactor = new_dwg.get_dxf_entity(reactor_handle)
    assert image.dxf.handle == reactor.dxf.owner, "IMAGE is not owner of IMAGEDEF_REACTOR"
    assert image.dxf.handle == reactor.dxf.image, "IMAGEDEF_REACTOR does not point to IMAGE"

    assert reactor_handle in image_def2.get_reactors(), "Reactor handle not in IMAGE_DEF reactors."

    # delete image
    msp.delete_entity(image)
    assert reactor_handle not in new_dwg.objects, "IMAGEDEF_REACTOR not deleted for objects load_section"
    assert reactor_handle not in new_dwg.entitydb, "IMAGEDEF_REACTOR not deleted for entity database"
    assert reactor_handle not in image_def2.get_reactors(), "Reactor handle not deleted from IMAGE_DEF reactors."


IMAGE_DEF = """  0
IMAGEDEF
  5
DEAD
330
DEAD
100
AcDbRasterImageDef
 90
        0
  1
mycat.jpg
 10
640.0
 20
360.0
 11
0.01
 21
0.01
280
     1
281
     0
"""

IMAGE = """  0
IMAGE
  5
1DF
330
1F
100
AcDbEntity
  8
0
100
AcDbRasterImage
 90
        0
 10
0.0
 20
0.0
 30
0.0
 11
0.01
 21
0.0
 31
0.0
 12
0.0
 22
0.01
 32
0.0
 13
640.0
 23
360.0
340
DEAD
 70
     7
280
     0
281
    50
282
    50
283
     0
360
DEAD
 71
     1
 91
        2
 14
0.
 24
0.
 14
640.
 24
360.
"""