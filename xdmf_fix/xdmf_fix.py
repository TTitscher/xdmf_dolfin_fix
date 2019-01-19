import os.path
import logging
from argparse import ArgumentParser
from . import fix
from . import convert
from . import files

def run(infile, outfile, dim=None):
    files.copy_with_src_ext(infile, outfile)

    name, ext = os.path.splitext(outfile)

    geo = name + ".geo"
    msh = name + ".msh"
    xdmf = name + ".xdmf"

    if ext == ".geo":
        logging.info(geo, "-->", msh)
        convert.geo_to_msh(geo, msh, dim)
        ext = ".msh"
    
    if ext == ".msh":
        logging.info(msh, "-->", xdmf)
        convert.msh_to_xdmf(msh, xdmf)

    logging.info("Fix", xdmf)
    fix.fix_ordering(xdmf)


def cli():
    p = ArgumentParser(description="Convert.")
    p.add_argument("infile")
    p.add_argument("outfile", nargs="?")
    p.add_argument("-d", "--dimension", type=int, default=None, choices=[2, 3])
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

    run(infile, outfile, dimension)


if __name__ == "__main__":
    cli()
