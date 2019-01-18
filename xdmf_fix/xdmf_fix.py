import os.path
import shutil
from argparse import ArgumentParser
from . import fix


def copy_xdmf(src, dest):
    """
    src ... xdmf file, with corresponding h5 file in same dir
    dest ... xdmf file. Creates a h5 with same name.
    """
    if src == dest:
        return

    src_name, src_ext = os.path.splitext(src)
    dest_name, dest_ext = os.path.splitext(dest)

    assert src_ext == ".xdmf"
    assert dest_ext == ".xdmf"

    # 1) copy xdmfs
    shutil.copy(src, dest)

    # 2) rename hdfs in dest
    hdf_src_base = fix.hdf_data_name(src)[0]
    hdf_dest_base = os.path.basename(dest_name) + ".h5"
    fix.replace_in_file(dest, hdf_src_base, hdf_dest_base)

    # 3) copy hdfs
    hdf_src = os.path.join(os.path.dirname(src), hdf_src_base)
    hdf_dest = os.path.join(os.path.dirname(dest), hdf_dest_base)
    shutil.copy(hdf_src, hdf_dest)


def cli():
    p = ArgumentParser(description="Convert.")
    p.add_argument("infile")
    p.add_argument("outfile")
    args = p.parse_args()

    copy_xdmf(args.infile, args.outfile)
    fix.fix_ordering(args.outfile)


if __name__ == "__main__":
    cli()
