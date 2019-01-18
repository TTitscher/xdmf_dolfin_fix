import os
import tempfile
import meshio


def _xdfm_from_geo_string(geo_string, name, dim):
    tmp = tempfile.mkdtemp()
    geo = os.path.join(tmp, name + ".geo")
    msh = os.path.join(tmp, name + ".msh")
    xdmf = os.path.join(name + ".xdmf")
    
    if os.path.isfile(xdmf):
        return xdmf

    with open(geo, "w") as f:
        f.write(geo_string)

    gmsh_cmd = "gmsh -{} -order 2 {}".format(dim, geo)
    os.system(gmsh_cmd)

    meshio.write(xdmf, meshio.read(msh))
    return xdmf


def triangle6():
    return _xdfm_from_geo_string(
        """
SetFactory("OpenCASCADE");
Rectangle(1) = {0, 0, 0, 1, 1, 0};
Physical Surface(1) = {1};
            """,
        "triangle",
        2,
    )


def tet10():
    return _xdfm_from_geo_string(
        """
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
Physical Volume(1) = {1};
            """,
        "tet10",
        3,
    )

if __name__ == "__main__":
    print(triangle6())
    print(tet10())
