import os
import re
import xml.etree.ElementTree as ET
import h5py
from tqdm import tqdm
from . import node_reordering

def replace_in_file(xdmf, search, replace):
    with open(xdmf, "r") as f:
        text = f.read()
        text = re.sub(search, replace, text, flags=re.IGNORECASE)
    with open(xdmf, "w") as f:
        f.write(text)


def hdf_data_name(xdmf):
    topology = ET.parse(xdmf).find(".//Topology/DataItem")

    if topology.attrib["Format"].lower() != "hdf":
        raise RuntimeError("Topology information must be in HDF format.")

    hdf, subset = topology.text.split(":")
    return hdf, subset

def fix_tet10(xdmf):
    replace_in_file(xdmf, "tetrahedron_10", "tet_10")
    return xdmf

def _element_type(xdmf):
    return ET.parse(xdmf).find(".//Topology").attrib["TopologyType"].lower()

def fix_ordering(xdmf):
    elm = _element_type(xdmf)

    if elm == "tetrahedron_10":
        fix_tet10(xdmf)
        elm = _element_type(xdmf) 
        assert elm == "tet_10"    
        
    if elm not in ["triangle_6", "tet_10"]:
        return

    hdf, subset = hdf_data_name(xdmf)
    hdf = os.path.join(os.path.dirname(xdmf), hdf)

    if elm == "triangle_6":
        reorder = node_reordering.triangle6
    else:
        reorder = node_reordering.tet10

    with h5py.File(hdf, "r+") as f:
        data = f[subset]
        data_array = data[...]

        swap = node_reordering.CountTheSwaps()
        for row in tqdm(data_array):
            reorder(row, swap)
        print("Reordering required {} swaps.".format(swap.n))
        
        # we do not change the shape...
        data[...] = data_array



