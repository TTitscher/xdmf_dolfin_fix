import unittest
import get_xdmf
from dolfin import XDMFFile, Mesh, Measure, assemble

def area(xdmf):
    mesh = Mesh()
    with XDMFFile(xdmf) as f:
        f.read(mesh)
    return assemble(1 * Measure('dx', mesh))

class TestXdmfFix(unittest.TestCase):
    
    triangle6 = get_xdmf.triangle6()
    tet10 = get_xdmf.tet10()


    def test_triangle_wrong(self):
        a = area(self.triangle6)
        self.assertNotAlmostEqual(a, 1.)
    
    def test_tet_wrong(self):
        self.assertRaises(RuntimeError, area, self.tet10) 
        # a = area(self.tet10)
        # print("Area without fix:", a)
        # self.assertNotAlmostEqual(a, 1.)


if __name__ == "__main__":
    unittest.main()
