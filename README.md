# xdmf_dolfin_fix

There is an xdmf import issue in FEniCS/DOLFIN. Quadratic triangles and tetrahedrons
are imported incorrectly. The CLI tool `xdmf-dolfin-fix` fixes this issue by reordering element numbers.

### Example usage
~~~
xdmf-dolfin-fix old.xdmf            # fix old.xdmf
xdmf-dolfin-fix old.xdmf new.xdmf   # create fixed new.xdmf
xdmf-dolfin-fix old.geo -d3         # create fixed old.xdmf from gmsh
xdmf-dolfin-fix old.msh new.xdmf    # create fixed new.xdmf from gmsh
~~~

### Problem

At some point of the simulation FEniCS/DOLFIN orders the vertices of all elements
in numerically accending order. Nodes on the edges of elements -- as present
in quadratic triangles and quadratic tetrahedrons -- are not swapped.

So internally, the node numbers of an arbitrary quadratic tetrahedron

~~~
[ vertices |    edges   ]
[ 51 74 12 | 14 72 1003 ]
~~~

would be reordered to

~~~
[ 12 51 74 | 14 72 1003 ]
~~~

Now, the vertex nodes `[12 51 74]` are sorted, but the edge nodes `[14 72 1003]`
are left unchanged. This results in a twisted geometry.

### Fix

`xdmf-dolfin-fix` sorts the vertex nodes **and** reorders the edge nodes accordingly. This
will result in

~~~
[ 12 51 74 | 1003 14 74 ]
~~~

A further sorting within DOLFIN has no effect and, thus, will not mess up
this ordering.


