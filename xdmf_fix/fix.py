def fix_tet10(xdmf):
    with open(xdmf, "r") as f:
        text = f.read().replace("Tetrahedron_10", "tet_10")
    with open(xdmf, "w") as f:
        f.write(text)
    return xdmf
