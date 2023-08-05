import ezdxf


def test_kit_dev_coldfire():
    dwg = ezdxf.readfile(r'D:\Source\dxftest\CADKitSamples\kit-dev-coldfire-xilinx_5213.dxf')
    auditor = dwg.auditor()
    errors = auditor.run()
    assert len(errors) == 0


def gkb_R2010():
    dwg = ezdxf.readfile(r'D:\Source\dxftest\GKB-R2010.dxf')
    auditor = dwg.audit()
    errors = auditor.run()
    assert len(errors) == 4

