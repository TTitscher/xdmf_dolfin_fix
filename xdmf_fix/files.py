import os
import shutil
import re
import xml.etree.ElementTree as ET

def _topology_info(xdmf):
    topology = ET.parse(xdmf).find(".//Topology/DataItem")

    if topology.attrib["Format"].lower() != "hdf":
        raise RuntimeError("Topology information must be in HDF format.")

    hdf, subset = topology.text.split(":")
    return hdf, subset

def topology_subset(xdmf):
    return _topology_info(xdmf)[1]

def h5_rel(xdmf):
    return _topology_info(xdmf)[0]

def h5_abs(xdmf):
    dirname = os.path.dirname(xdmf)
    return os.path.join(dirname, h5_rel(xdmf))


def element_type(xdmf):
    return ET.parse(xdmf).find(".//Topology").attrib["TopologyType"].lower()


def replace(xdmf, search, replace):
    with open(xdmf, "r") as f:
        text = f.read()
        text = re.sub(search, replace, text, flags=re.IGNORECASE)
    with open(xdmf, "w") as f:
        f.write(text)


def copy_xdmf(src, dest):
    """
    src ... xdmf file, with corresponding h5 file in same dir
    dest ... xdmf file. Creates a h5 with same name.
    """

    # 1) copy xdmfs
    shutil.copy(src, dest)

    # 2) rename hdfs in dest
    hdf_src_base = h5_rel(src)

    dest_name = os.path.splitext(dest)[0]
    hdf_dest_base = os.path.basename(dest_name) + ".h5"
    replace(dest, hdf_src_base, hdf_dest_base)

    # 3) copy hdfs
    hdf_src = os.path.join(os.path.dirname(src), hdf_src_base)
    hdf_dest = os.path.join(os.path.dirname(dest), hdf_dest_base)
    shutil.copy(hdf_src, hdf_dest)

def copy_with_src_ext(infile, outfile):
    src_name, src_ext = os.path.splitext(infile)
    dest_name, dest_ext = os.path.splitext(outfile)

    if src_name == dest_name:
        return

    if src_ext == ".xdmf":
        copy_xdmf(infile, outfile)
    else:
        shutil.copy(infile, dest_name + src_ext)

