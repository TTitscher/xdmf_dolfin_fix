from subprocess import PIPE, Popen
import logging

def geo_to_msh(geo, msh, dim):
    """
    Meshes the .geo file `geo` into the .msh file `msh` using the gmsh CLI.
    """
    logging.info("{} --> {}".format(geo, msh))

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
    import meshio    # optional dependency
    
    logging.info("{} --> {}".format(msh, xdmf))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        meshio.write(xdmf, meshio.read(msh))
