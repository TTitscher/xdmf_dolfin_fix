import os.path
import logging
from argparse import ArgumentParser

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
    p = ArgumentParser(description="Convert.")
    p.add_argument("infile")
    p.add_argument("outfile", nargs="?")
    p.add_argument("-d", "--dimension", type=int, default=None, choices=[2, 3])
    p.add_argument("-v", "--verbose", action="count", default=0)
    args = p.parse_args()

    infile = args.infile
    if not os.path.exists(infile):
        raise RuntimeError("'Cannot open '{}'. Please provide a valid "
                           "input file.".format(infile))
    
    outfile = args.outfile
    if outfile is None:
        outfile = infile # perform everything in place
   
    dimension = args.dimension
    if os.path.splitext(infile)[1] == ".geo" and dimension is None:
        raise RuntimeError("Specifiy '-d, --dimension' for '.geo' files.")

    if args.verbose == 0:
        log_level = logging.ERROR
    if args.verbose == 1:
        log_level = logging.WARNING
    if args.verbose == 2:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, 
            format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    run(infile, outfile, dimension)

if __name__ == "__main__":
    cli()
