from subprocess import PIPE, Popen
import logging
import numpy
import shutil


def geo_to_msh(geo, msh, dim):
    """
    Meshes the .geo file `geo` into the .msh file `msh` using the gmsh CLI.
    """
    if shutil.which("gmsh") is None:
        raise RuntimeError(
            "You have to provide the 'gmsh' executable in your PATH to use this feature."
        )

    gmsh_cmd = ["gmsh", "-" + str(dim), "-order", "2", geo, "-o", msh]
    p = Popen(gmsh_cmd, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    logging.debug(output.decode("utf-8"))
    if err:
        logging.error(err.decode("utf-8"))


def msh_to_xdmf(msh, xdmf):
    """
    Convert the .msh file `msh` to the .xdmf file `xdmf` using meshio. 
    """
    import warnings
    import meshio  # optional dependency

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mesh = meshio.read(msh)
        # cli option -z --prune-z from
        # https://github.com/nschloe/meshio/blob/a2b733511e943e337d7230403091d12daa0874cc/meshio/cli.py#L28
        if mesh.points.shape[1] == 3 and numpy.all(
            numpy.abs(mesh.points[:, 2]) < 1.0e-10
        ):
            mesh.points = mesh.points[:, :2]

        meshio.write(xdmf, mesh)
