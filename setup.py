import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xdmf-dolfin-fix",
    version="0.6.2",
    author="Thomas Titscher",
    author_email="thomas.titscher@gmail.com",
    description="A tiny package to modify the node order of quadratic triangles and tets in a xdmf-hdf mesh to work with FEniCS/DOLFIN.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TTitscher/xdmf_dolfin_fix",
    packages=["xdmf_dolfin_fix"],
    install_requires=["h5py", "lxml", "meshio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["xdmf-dolfin-fix=xdmf_dolfin_fix.cli:cli"]}
)
