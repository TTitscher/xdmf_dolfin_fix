import os.path
import sys
import shutil
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

from .xdmf_mesh import XDMFMesh
from . import convert

def log_conversion(a, b):
    logging.info("{:^20} --> {:^20}".format(a, b))


def copy(infile, outfile, ext):
    if infile == outfile:
        return

    log_conversion(infile, outfile)
    if ext == ".xdmf":
        XDMFMesh(infile).copy(outfile)
    else:
        shutil.copy(infile, outfile)


def run(infile, outfile, dim=None):
    """
    Copies the infile 
        (<in_name><in_ext>) 
    to 
        (<out_name><in_ext>)

    and performs the conversion chain
    <out_name>.geo --> <out_name>.msh --> <out_name>.xdmf --> <out_name>.xdmf(DOLFIN)
    in-place. The starting point of this chain depends on <in_ext>.


    infile:
        File name of the input file. Ends with .geo, .msh or .xdmf.

    outfile:
        File name of the output file. Ends with .xdmf.

    dim:
        Global dimension of the mesh. dim != None required for infile = .geo
    """

    name = os.path.splitext(outfile)[0]
    infile_ext = os.path.splitext(infile)[1]

    copy(infile, name+infile_ext, infile_ext)

    geo = name + ".geo"
    msh = name + ".msh"
    xdmf = name + ".xdmf"
    
    if infile_ext == ".geo":
        log_conversion(geo, msh)
        convert.geo_to_msh(geo, msh, dim)
        infile_ext = ".msh"

    if infile_ext == ".msh":
        log_conversion(msh, xdmf)
        convert.msh_to_xdmf(msh, xdmf)

    logging.info("Sort vertices in {}".format(xdmf))
    XDMFMesh(xdmf).fix_ordering()

def setup_logger(v):
    if v == 0:
        log_level = logging.WARNING
    elif v == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def cli():
    extensions = [".geo", ".msh", ".xdmf"]

    p = ArgumentParser(
        description="""
    Changes a XDMF mesh containing quadratic triangles/tetrahedrons to 
    properly work with FEniCS/DOLFIN.

    Meshes in XDMF format are the only way to import quadratic elements
    into FEniCS/DOLFIN. DOLFIN performs a renumbering (sort) of the vertex 
    nodes without changing the edge nodes accordingly. `xdmf-fix` performs
    a consistent node renumbering so the DOLFIN vertex sort has no effect
    on the mesh. 
    
    OPTIONALY: Depending on the input file format, every step in the chain
    [.geo]  --gmsh-->  [.msh]  --meshio-->  [.xdmf]  --xdmf-fix-->  [.xdmf]
    can be performed.
    """,
        formatter_class=RawTextHelpFormatter,
    )

    p.add_argument("infile", help="Input file in {} format.".format(extensions))
    p.add_argument(
        "outfile", nargs="?", help="OPTIONAL: Output file. Defaults to `infile`."
    )
    p.add_argument(
        "-d",
        "--dimension",
        type=int,
        default=None,
        choices=[2, 3],
        help="Optional input to gmsh.",
    )
    p.add_argument("-v", help="show warnings(), info(-v) or debug(-vv).", action="count", default=0)
    args = p.parse_args()

    setup_logger(args.v)

    infile = args.infile
    outfile = args.outfile
    if outfile is None:
        outfile = infile  # perform everything in place

    if not os.path.exists(infile):
        logging.error(
            "Cannot open '{}'. Please provide a valid input file.".format(infile)
        )
        sys.exit(1)

    if os.path.splitext(infile)[1] not in extensions:
        logging.error("Invalid input file format. Use {}.".format(extensions))
        sys.exit(1)

    if os.path.splitext(outfile)[1] != ".xdmf":
        logging.error("Output must be in .xdmf format.")
        sys.exit(1)

    dimension = args.dimension
    if os.path.splitext(infile)[1] == ".geo" and dimension is None:
        logging.error("Specifiy '-d, --dimension' for '.geo' files.")
        sys.exit(1)

    run(infile, outfile, dimension)


if __name__ == "__main__":
    cli()
