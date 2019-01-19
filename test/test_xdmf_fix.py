import os
import unittest
import tempfile

import get_xdmf
import test_context
from xdmf_fix import fix, files

from dolfin import XDMFFile, Mesh, Measure, assemble


def area(xdmf):
    mesh = Mesh()
    with XDMFFile(xdmf) as f:
        f.read(mesh)
    return assemble(1 * Measure("dx", mesh))


# class TestXdmfFix(unittest.TestCase):
#     def test_triangle_area(self):
#         triangle = get_xdmf.triangle6()
#         self.assertNotAlmostEqual(area(triangle), 1.0)
#
#         fix.fix_ordering(triangle)
#         self.assertAlmostEqual(area(triangle), 1.0)
#
#     def test_tet_area(self):
#         tet = fix.fix_tet10(get_xdmf.tet10())
#         self.assertNotAlmostEqual(area(tet), 1.0)
#
#         fix.fix_ordering(tet)
#         self.assertAlmostEqual(area(tet), 1.0)
#
#     def test_fix_tet10(self):
#         tet = get_xdmf.tet10()
#         self.assertRaises(RuntimeError, area, tet)
#
#         fix.fix_tet10(tet)
#         area(tet)

class TestFileCopy(unittest.TestCase):
    def test_geo(self):
        tmp = tempfile.mkdtemp()
        infile = os.path.join(tmp, "a.geo")
        open(infile, "w").close()  # touch

        outfile = os.path.join(tmp, "b.xdmf")
        expected = os.path.join(tmp, "b.geo")
        files.copy_with_src_ext(infile, outfile)
        self.assertTrue(os.path.exists(expected))

    def test_msh(self):
        tmp = tempfile.mkdtemp()
        infile = os.path.join(tmp, "a.msh")
        open(infile, "w").close()  # touch

        outfile = os.path.join(tmp, "b.xdmf")
        expected = os.path.join(tmp, "b.msh")
        files.copy_with_src_ext(infile, outfile)
        self.assertTrue(os.path.exists(expected))

    def test_xdmf(self):
        tmp = tempfile.mkdtemp()
        infile = get_xdmf.triangle6()
        outfile = os.path.join(tmp, "b.xdmf")
        files.copy_with_src_ext(infile, outfile)

        expected_h5 = os.path.join(tmp, "b.h5")
        self.assertTrue(os.path.exists(outfile))
        self.assertTrue(os.path.exists(expected_h5))


if __name__ == "__main__":
    unittest.main()
