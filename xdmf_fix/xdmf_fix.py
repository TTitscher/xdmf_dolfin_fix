import os.path
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

from .xdmf_mesh import XDMFMesh
from . import convert

def copy_with_src_ext(infile, outfile):
    src_name, src_ext = os.path.splitext(infile)
    dest_name, dest_ext = os.path.splitext(outfile)

    if src_name == dest_name:
        return
    
    logging.info("{} --> {}".format(infile, dest_name + src_ext))

    if src_ext == ".xdmf":
        XDMFMesh(infile).copy(outfile)
    else:
        shutil.copy(infile, dest_name + src_ext)


def run(infile, outfile, dim=None):
    copy_with_src_ext(infile, outfile)

    name, ext = os.path.splitext(outfile)

    geo = name + ".geo"
    msh = name + ".msh"
    xdmf = name + ".xdmf"

    if ext == ".geo":
        convert.geo_to_msh(geo, msh, dim)
        ext = ".msh"
    
    if ext == ".msh":
        convert.msh_to_xdmf(msh, xdmf)

    logging.info("Sort vertices in {}".format(xdmf))
    XDMFMesh(xdmf).fix_ordering()


def cli():
    extensions = [".geo", ".msh", ".xdmf"]

    p = ArgumentParser(description="""
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
    """, formatter_class=RawTextHelpFormatter)

    p.add_argument("infile", help="Input file in {} format.".format(extensions))
    p.add_argument("outfile", nargs="?", help="OPTIONAL: Output file. Defaults to `infile`.")
    p.add_argument("-d", "--dimension", type=int, default=None, choices=[2, 3], help="Optional input to gmsh.")
    p.add_argument("-v", help="show for warnings.", action='store_true')
    p.add_argument("-vv", help="show every output.", action='store_true')
    args = p.parse_args()

    infile = args.infile
    outfile = args.outfile
    if outfile is None:
        outfile = infile # perform everything in place

    if not os.path.exists(infile):
        raise RuntimeError("'Cannot open '{}'. Please provide a valid "
                           "input file.".format(infile))
    
    if os.path.splitext(infile)[1] not in extensions:
        raise RuntimeError("Invalid input file format. Use {}.".format(extensions))
    
    if os.path.splitext(outfile)[1] != ".xdmf":
        raise RuntimeError("Output must be in .xdmf format.")

    dimension = args.dimension
    if os.path.splitext(infile)[1] == ".geo" and dimension is None:
        raise RuntimeError("Specifiy '-d, --dimension' for '.geo' files.")
        
    
    log_level = logging.ERROR 
    if args.vv:
        log_level = logging.DEBUG 
    elif args.v:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level, 
            format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    run(infile, outfile, dimension)

if __name__ == "__main__":
    cli()
