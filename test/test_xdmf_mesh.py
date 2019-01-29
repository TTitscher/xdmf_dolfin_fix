import os
import unittest
import tempfile

from dolfin import XDMFFile, Mesh, Measure, assemble

import test_context
from xdmf_dolfin_fix.xdmf_mesh import XDMFMesh
from xdmf_dolfin_fix import convert
    
tmp = tempfile.mkdtemp()
    
def _xdfm_from_geo_string(geo_string, name, dim):
    xdmf = name + ".xdmf"
    if os.path.exists(xdmf):
        return xdmf

    geo = os.path.join(tmp, name + ".geo")
    msh = os.path.join(tmp, name + ".msh")

    with open(geo, "w") as f:
        f.write(geo_string)

    convert.geo_to_msh(geo, msh, dim)
    convert.msh_to_xdmf(msh, xdmf)
    return xdmf


def xdmf_triangle():
    return _xdfm_from_geo_string(
        """
SetFactory("OpenCASCADE");
Rectangle(1) = {0, 0, 0, 1, 1, 0};
Physical Surface(1) = {1};
            """,
        "triangle6",
        2,
    )


def xdmf_tet10():
    return _xdfm_from_geo_string(
        """
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
Physical Volume(1) = {1};
            """,
        "tet10",
        3,
    )

def area(xdmf):
    mesh = Mesh()
    with XDMFFile(xdmf) as f:
        f.read(mesh)
    return assemble(1 * Measure("dx", mesh))

def tmp_name(name, ext = ".xdmf"):
    return os.path.join(tmp, name + ext)


class TestXDMFMesh(unittest.TestCase):

    def test_copy(self):
        infile = xdmf_triangle()
        out = tmp_name("copy")
        out_h5 = tmp_name("copy", ".h5")

        XDMFMesh(infile).copy(out)

        self.assertTrue(os.path.exists(out))
        self.assertTrue(os.path.exists(out_h5))

    def test_triangle_area(self):
        triangle = xdmf_triangle()
        self.assertNotAlmostEqual(area(triangle), 1.0)

        XDMFMesh(triangle).copy(tmp_name("tri")).fix_ordering()
        self.assertAlmostEqual(area(tmp_name("tri")), 1.0)

    def test_fix_tet10(self):
        tet = xdmf_tet10()
        self.assertRaises(RuntimeError, area, tet)

        XDMFMesh(tet).copy(tmp_name("fix_tet10")).fix_tet10()
        area(tmp_name("fix_tet10"))
    
    def test_tet_area(self):
        tet = xdmf_tet10()
        
        XDMFMesh(tet).copy(tmp_name("fix_tet10")).fix_tet10()
        self.assertNotAlmostEqual(area(tmp_name("fix_tet10")), 1.0)

        XDMFMesh(tet).copy(tmp_name("tet")).fix_ordering()
        self.assertAlmostEqual(area(tmp_name("tet")), 1.0)


if __name__ == "__main__":
    unittest.main()
