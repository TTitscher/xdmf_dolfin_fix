import logging
import h5py
from . import files
from . import node_reordering


def fix_tet10(xdmf):
    files.replace(xdmf, "tetrahedron_10", "tet_10")
    return xdmf


def fix_ordering(xdmf):
    elm = files.element_type(xdmf)

    if elm == "tetrahedron_10":
        fix_tet10(xdmf)
        elm = files.element_type(xdmf)
        assert elm == "tet_10"

    if elm not in ["triangle_6", "tet_10"]:
        return

    subset = files.topology_subset(xdmf)

    with h5py.File(files.h5_abs(xdmf), "r+") as f:
        data = f[subset]
        data_array = data[...]

        if elm == "triangle_6":
            n_swaps = node_reordering.triangle6(data_array)
        else:
            n_swaps = node_reordering.tet10(data_array)

        logging.info("Reordering required {} swaps.".format(n_swaps))

        # we do not change the shape...
        data[...] = data_array
