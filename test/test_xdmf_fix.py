import unittest
import get_xdmf
import test_context
from xdmf_fix import fix

from dolfin import XDMFFile, Mesh, Measure, assemble


def area(xdmf):
    mesh = Mesh()
    with XDMFFile(xdmf) as f:
        f.read(mesh)
    return assemble(1 * Measure("dx", mesh))


class TestXdmfFix(unittest.TestCase):
    def test_triangle_area(self):
        triangle = get_xdmf.triangle6()
        self.assertNotAlmostEqual(area(triangle), 1.0)

        fix.fix_ordering(triangle)
        self.assertAlmostEqual(area(triangle), 1.0)

    def test_tet_area(self):
        tet = fix.fix_tet10(get_xdmf.tet10())
        self.assertNotAlmostEqual(area(tet), 1.0)
        
        fix.fix_ordering(tet)
        self.assertAlmostEqual(area(tet), 1.0)

    def test_fix_tet10(self):
        tet = get_xdmf.tet10()
        self.assertRaises(RuntimeError, area, tet)

        fix.fix_tet10(tet)
        area(tet)
    

if __name__ == "__main__":
    unittest.main()
