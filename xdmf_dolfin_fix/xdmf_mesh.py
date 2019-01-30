import os
import re
import shutil
import logging
from lxml import etree as ET
import h5py

from . import node_reordering

class XDMFMesh:
    def __init__(self, xdmf):
        self.xdmf = xdmf

        topology_node = ET.parse(xdmf).find(".//Topology")
        self.element_type = topology_node.attrib["TopologyType"].lower()

        if self.topology_data_node().attrib["Format"].lower() != "hdf":
            raise RuntimeError("Topology information must be in HDF format.")

    def replace_string(self, search, replace):
        with open(self.xdmf, "r") as f:
            text = f.read()
            text = re.sub(search, replace, text, flags=re.IGNORECASE)
        with open(self.xdmf, "w") as f:
            f.write(text)

    def fix_tet10(self):
        if self.element_type == "tetrahedron_10":
            self.replace_string("tetrahedron_10", "tet_10")
            self.element_type = "tet_10"

    def topology_data_node(self):
        return ET.parse(self.xdmf).find(".//Topology/DataItem")

    def h5(self):
        return self.topology_data_node().text.split(':')[0]

    def topology_dataset(self):
        return self.topology_data_node().text.split(':')[1]

    def fix_ordering(self):
        if self.element_type not in ["triangle_6", "tet_10", "tetrahedron_10"]:
            return

        self.fix_tet10()

        dirname = os.path.dirname(self.xdmf)
        h5 = os.path.join(dirname, self.h5())

        with h5py.File(h5, "r+") as f:
            data = f[self.topology_dataset()]
            data_array = data[...]

            if self.element_type == "triangle_6":
                n_swaps = node_reordering.triangle6(data_array)
            else:
                n_swaps = node_reordering.tet10(data_array)

            logging.info("Sort vertices required {} swaps.".format(n_swaps))

            # we do not change the shape...
            data[...] = data_array

    def copy(self, dest):
        """
        dest ... xdmf file. Creates a h5 with same name.
        """

        # 1) copy xdmfs
        shutil.copy(self.xdmf, dest)
        xdmf_mesh_new = XDMFMesh(dest)

        # 2) rename h5s in new xdmf mesh
        dest_basename = os.path.basename(dest)
        h5_dest_base = os.path.splitext(dest_basename)[0] + ".h5"
        xdmf_mesh_new.replace_string(self.h5(), h5_dest_base)

        # 3) copy hdfs
        hdf_src = os.path.join(os.path.dirname(self.xdmf), self.h5())
        hdf_dest = os.path.join(os.path.dirname(dest), h5_dest_base)
        shutil.copy(hdf_src, hdf_dest)

        return xdmf_mesh_new

