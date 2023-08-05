
ezdxf
=====

.. image:: https://readthedocs.org/projects/pip/badge/
   :target: https://ezdxf.readthedocs.io
   :alt: Read The Docs

Abstract
--------

A Python package to create and modify DXF drawings, independent from the DXF
version. You can open/save every DXF file without loosing any content (except comments),
Unknown tags in the DXF file will be ignored but preserved for saving. With this behavior
it is possible to open also DXF drawings that contains data from 3rd party applications.

Quick-Info
----------

- ezdxf is a Python package to create new DXF files and read/modify/write existing DXF files
- the intended audience are developers
- requires Python 2.7 or later, runs on CPython and pypy, maybe on IronPython and Jython
- OS independent
- additional required packages: `pyparsing <https://pypi.python.org/pypi/pyparsing/2.0.1>`_
- MIT-License
- read/write/new support for DXF versions: R12, R2000, R2004, R2007, R2010, R2013 and R2018
- additional read support for DXF versions R13/R14 (upgraded to R2000)
- additional read support for older DXF versions than R12 (upgraded to R12)
- preserves third-party DXF content
- additional fast DXF R12 writer, that creates just an ENTITIES section with support for the basic DXF entities

a simple example::

    import ezdxf

    drawing = ezdxf.new(dxfversion='AC1024')  # or use the AutoCAD release name ezdxf.new(dxfversion='R2010')
    modelspace = drawing.modelspace()
    modelspace.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
    drawing.layers.new('TEXTLAYER', dxfattribs={'color': 2})
    # use set_pos() for proper TEXT alignment - the relations between halign, valign, insert and align_point are tricky.
    modelspace.add_text('Test', dxfattribs={'layer': 'TEXTLAYER'}).set_pos((0, 0.2), align='CENTER')
    drawing.saveas('test.dxf')

example for the *r12writer*, writes a simple DXF R12 file without in-memory structures::

    from random import random
    from ezdxf.r12writer import r12writer

    MAX_X_COORD = 1000.0
    MAX_Y_COORD = 1000.0
    CIRCLE_COUNT = 100000

    with r12writer("many_circles.dxf") as dxf:
        for i in range(CIRCLE_COUNT):
            dxf.add_circle((MAX_X_COORD*random(), MAX_Y_COORD*random()), radius=2)

The r12writer supports only the ENTITIES section of a DXF R12 drawing, no HEADER, TABLES or BLOCKS section is
present, except FIXED-TABLES are written, than some additional predefined text styles and line types are available.

Installation
============

Install with pip::

    pip install ezdxf

or from source::

    python setup.py install

Website
=======

https://ezdxf.mozman.at/

Documentation
=============

Documentation of development version at https://ezdxf.mozman.at/docs

Documentation of latest release at http://ezdxf.readthedocs.io/

The source code of ezdxf can be found at GitHub.com:

http://github.com/mozman/ezdxf.git

Feedback
========

Issue Tracker at:

http://github.com/mozman/ezdxf/issues

Questions and Feedback at Google Groups:

https://groups.google.com/d/forum/python-ezdxf

python-ezdxf@googlegroups.com

Feedback is greatly appreciated.

Manfred

Contact
=======

ezdxf@mozman.at

News
====

Version 0.8.6 - 2018-02-17

   * NEW: ezdxf project website: https://ezdxf.mozman.at/
   * CHANGE: create all missing tables of the TABLES sections for DXF R12
   * BUGFIX: entities on new layouts will be saved
   * NEW: Layout.page_setup() and correct 'main' viewport for DXF R2000+; For DXF R12 page_setup() exists, but does not
     provide useful results. Page setup for DXF R12 is still a mystery to me.
   * NEW: Table(), MText(), Ellipse(), Spline(), Bezier(), Clothoid(), LinearDimension(), RadialDimension(),
     ArcDimension() and AngularDimension() composite objects from dxfwrite as addons, these addons support DXF R12
   * NEW: geometry builder as addons: MeshBuilder(), MeshVertexMerger(), MengerSponge(), SierpinskyPyramid(), these
     addons require DXF R2000+ (MESH entity)
   * BUGFIX: fixed invalid implementation of context manager for r12writer

Version 0.8.5 - 2018-01-28

   * CHANGE: block names are case insensitive 'TEST' == 'Test' (like AutoCAD)
   * CHANGE: table entry (layer, linetype, style, dimstyle, ...) names are case insensitive 'TEST' == 'Test' (like AutoCAD)
   * CHANGE: raises DXFInvalidLayerName() for invalid characters in layer names: <>/\":;?*|=`
   * CHANGE: audit process rewritten
   * CHANGE: skip all comments, group code 999
   * CHANGE: removed compression for unused sections (THUMBNAILSECTION, ACDSDATA)
   * NEW: write DXF R12 files without handles: set dwg.header['$HANDLING']=0, default value is 1
   * added subclass marker filter for R12 and prior files in legacy_mode=True (required for malformed DXF files)
   * removed special check for Leica Disto Unit files, use readfile(filename, legacy_mode=True) (malformed DXF R12 file,
     see previous point)

Version 0.8.4 - 2018-01-14

  * NEW: Support for complex line types with text or shapes
  * NEW: DXF file structure validator at SECTION level, tags outside of sections will be removed
  * NEW: Basic read support for DIMENSION
  * CHANGE: improved exception management, in the future ezdxf should only raise exceptions inherited from DXFError for
    DXF related errors, previous exception classes still work

    - DXFValueError(DXFError, ValueError)
    - DXFKeyError(DXFError, KeyError)
    - DXFAttributeError(DXFError, AttributeError)
    - DXFIndexError(DXFError, IndexError)
    - DXFTableEntryError(DXFValueError)

  * speedup low level tag reader around 5%, and speedup tag compiler around 5%

Version 0.8.3 - 2018-01-02

  * CHANGE: Lwpolyline - suppress yielding z coordinates if they exists (DXFStructureError: z coordinates are not defined in the DXF standard)
  * NEW: setup creates a script called 'dxfpp' (DXF Pretty Printer) in the Python script folder
  * NEW: basic support for DXF format AC1032 introduced by AutoCAD 2018
  * NEW: ezdxf use logging and writes all logs to a logger called 'ezdxf'. Logging setup is the domain of the application!
  * NEW: warns about multiple block definitions with the same name in a DXF file. (DXFStructureError)
  * NEW: legacy_mode parameter in ezdxf.read() and ezdxf.readfile(): tries do fix coordinate order in LINE
    entities (10, 11, 20, 21) by the cost of around 5% overall speed penalty at DXF file loading

Version 0.8.2 - 2017-05-01

  * NEW: Insert.delete_attrib(tag) - delete ATTRIB entities from the INSERT entity
  * NEW: Insert.delete_all_attribs() - delete all ATTRIB entities from the INSERT entity
  * BUGFIX: setting attribs_follow=1 at INSERT entity before adding an attribute entity works

Version 0.8.1 - 2017-04-06

  * NEW: added support for constant ATTRIB/ATTDEF to the INSERT (block reference) entity
  * NEW: added ATTDEF management methods to BlockLayout (has_attdef, get_attdef, get_attdef_text)
  * NEW: added (read/write) properties to ATTDEF/ATTRIB for setting flags (is_const, is_invisible, is_verify, is_preset)

Version 0.8.0 - 2017-03-28

  * added groupby(dxfattrib='', key=None) entity query function, it is supported by all layouts and the query result
    container: Returns a dict, where entities are grouped by a dxfattrib or the result of a key function.
  * added ezdxf.audit() for DXF error checking for drawings created by ezdxf - but not very capable yet
  * dxfattribs in factory functions like add_line(dxfattribs=...), now are copied internally and stay unchanged, so they
    can be reused multiple times without getting modified by ezdxf.
  * removed deprecated Drawing.create_layout() -> Drawing.new_layout()
  * removed deprecated Layouts.create() -> Layout.new()
  * removed deprecated Table.create() -> Table.new()
  * removed deprecated DXFGroupTable.add() -> DXFGroupTable.new()
  * BUFIX in EntityQuery.extend()

Version 0.7.9 - 2017-01-31

  * BUGFIX: lost data if model space and active layout are called \*MODEL_SPACE and \*PAPER_SPACE

Version 0.7.8 - 2017-01-22

  * BUGFIX: HATCH accepts SplineEdges without defined fit points
  * BUGFIX: fixed universal line ending problem in ZipReader()
  * Moved repository to GitHub: https://github.com/mozman/ezdxf.git

Version 0.7.7 - 2016-10-22

  * NEW: repairs malformed Leica Disto DXF R12 files, ezdxf saves a valid DXF R12 file.
  * NEW: added Layout.unlink(entity) method: unlinks an entity from layout but does not delete entity from the drawing database.
  * NEW: added Drawing.add_xref_def(filename, name) for adding external reference definitions
  * CHANGE: renamed parameters for EdgePath.add_ellipse() - major_axis_vector -> major_axis; minor_axis_length -> ratio
    to be consistent to the ELLIPSE entity
  * UPDATE: Entity.tags.new_xdata() and Entity.tags.set_xdata() accept tuples as tags, no import of DXFTag required
  * UPDATE: EntityQuery to support both 'single' and "double" quoted strings - Harrison Katz <harrison@neadwerx.com>
  * improved DXF R13/R14 compatibility

Version 0.7.6 - 2016-04-16

  * NEW: r12writer.py - a fast and simple DXF R12 file/stream writer. Supports only LINE, CIRCLE, ARC, TEXT, POINT,
    SOLID, 3DFACE and POLYLINE. The module can be used without ezdxf.
  * NEW: Get/Set extended data on DXF entity level, add and retrieve your own data to DXF entities
  * NEW: Get/Set app data on DXF entity level (not important for high level users)
  * NEW: Get/Set/Append/Remove reactors on DXF entity level (not important for high level users)
  * CHANGE: using reactors in PdfDefinition for well defined UNDERLAY entities
  * CHANGE: using reactors and IMAGEDEF_REACTOR for well defined IMAGE entities
  * BUGFIX: default name=None in add_image_def()

Version 0.7.5 - 2016-04-03

  * NEW: Drawing.acad_release property - AutoCAD release number for the drawing DXF version like 'R12' or 'R2000'
  * NEW: support for PDFUNDERLAY, DWFUNDERLAY and DGNUNDERLAY entities
  * BUGFIX: fixed broken layout setup in repair routine
  * BUGFIX: support for utf-8 encoding on saving, DXF R2007 and later is saved with UTF-8 encoding
  * CHANGE: Drawing.add_image_def(filename, size_in_pixel, name=None), renamed key to name and set name=None for auto-generated internal image name
  * CHANGE: argument order of Layout.add_image(image_def, insert, size_in_units, rotation=0., dxfattribs=None)

Version 0.7.4 - 2016-03-13

  * NEW: support for DXF entity IMAGE (work in progress)
  * NEW: preserve leading file comments (tag code 999)
  * NEW: writes saving and upgrading comments when saving DXF files; avoid this behavior by setting options.store_comments = False
  * NEW: ezdxf.new() accepts the AutoCAD release name as DXF version string e.g. ezdxf.new('R12') or R2000, R2004, R2007, ...
  * NEW: integrated acadctb.py module from my dxfwrite package to read/write AutoCAD .ctb config files; no docs so far
  * CHANGE: renamed Drawing.groups.add() to new() for consistent name schema for adding new items to tables (public interface)
  * CHANGE: renamed Drawing.<tablename>.create() to new() for consistent name schema for adding new items to tables,
    this applies to all tables: layers, styles, dimstyles, appids, views, viewports, ucs, block_records. (public interface)
  * CHANGE: renamed Layouts.create() to new() for consistent name schema for adding new items to tables (internal interface)
  * CHANGE: renamed Drawing.create_layout() to new_layout() for consistent name schema for adding new items (public interface)
  * CHANGE: renamed factory method <layout>.add_3Dface() to add_3dface()
  * REMOVED: logging and debugging options
  * BUGFIX: fixed attribute definition for align_point in DXF entity ATTRIB (AC1015 and newer)
  * Cleanup DXF template files AC1015 - AC1027, file size goes down from >60kb to ~20kb

Version 0.7.3 - 2016-03-06

  * Quick bugfix release, because ezdxf 0.7.2 can damage DXF R12 files when saving!!!
  * NEW: improved DXF R13/R14 compatibility
  * BUGFIX: create CLASSES section only for DXF versions newer than R12 (AC1009)
  * TEST: converted a bunch of R8 (AC1003) files to R12 (AC1009), AutoCAD didn't complain
  * TEST: converted a bunch of R13 (AC1012) files to R2000 (AC1015), AutoCAD didn't complain
  * TEST: converted a bunch of R14 (AC1014) files to R2000 (AC1015), AutoCAD didn't complain

Version 0.7.2 - 2016-03-05

  * NEW: reads DXF R13/R14 and saves content as R2000 (AC1015) - experimental feature, because of the lack of test data
  * NEW: added support for common DXF attribute line weight
  * NEW: POLYLINE, POLYMESH - added properties is_closed, is_m_closed, is_n_closed
  * BUGFIX: MeshData.optimize() - corrected wrong vertex optimization
  * BUGFIX: can open DXF files without existing layout management table
  * BUGFIX: restore module structure ezdxf.const

Version 0.7.1 - 2016-02-21

  * Supported/Tested Python versions: CPython 2.7, 3.4, 3.5, pypy 4.0.1 and pypy3 2.4.0
  * NEW: read legacy DXF versions older than AC1009 (DXF R12) and saves it as DXF version AC1009.
  * NEW: added methods is_frozen(), freeze(), thaw() to class Layer()
  * NEW: full support for DXF entity ELLIPSE (added add_ellipse() method)
  * NEW: MESH data editor - implemented add_face(vertices), add_edge(vertices), optimize(precision=6) methods
  * BUGFIX: creating entities on layouts works
  * BUGFIX: entity ATTRIB - fixed halign attribute definition
  * CHANGE: POLYLINE (POLYFACE, POLYMESH) - on layer change also change layer of associated VERTEX entities

Version 0.7.0 - 2015-11-26

  * Supported Python versions: CPython 2.7, 3.4, pypy 2.6.1 and pypy3 2.4.0
  * NEW: support for DXF entity HATCH (solid fill, gradient fill and pattern fill), pattern fill with background color supported
  * NEW: support for DXF entity GROUP
  * NEW: VIEWPORT entity, but creating new viewports does not work as expected - just for reading purpose.
  * NEW: support for new common DXF attributes in AC1018 (AutoCAD 2004): true_color, color_name, transparency
  * NEW: support for new common DXF attributes in AC1021 (AutoCAD 2007): shadow_mode
  * NEW: extended custom vars interface
  * NEW: dxf2html - added support for custom properties in the header section
  * NEW: query() supports case insensitive attribute queries by appending an 'i' to the query string, e.g. '\*[layer=="construction"]i'
  * NEW: Drawing.cleanup() - call before saving the drawing but only if necessary, the process could take a while.
  * BUGFIX: query parser couldn't handle attribute names containing '_'
  * CHANGE: renamed dxf2html to pp (pretty printer), usage: py -m ezdxf.pp yourfile.dxf (generates yourfile.html in the same folder)
  * CHANGE: cleanup file structure



