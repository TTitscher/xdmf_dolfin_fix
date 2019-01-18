class CountTheSwaps:
    def __init__(self):
        self.n = 0

    def __call__(self, n, a, b):
        n[a], n[b] = n[b], n[a]
        self.n += 1


def tet10(n, swap):
    r"""
    Reorder the vertex nodes so that n[0] < n[1] < n[2] < n[4].
    The order of the edge nodes n[4:10] is changed such that the cells
    still form a valid Tet10.

    Tetrahedron10:

                   v
                 .
               ,/
              /
           2
         ,/|`\
       ,/  |  `\
     ,6    '.   `5
   ,/       9     `\
 ,/         |       `\
0--------4--'.--------1 --> u
 `\.         |      ,/
    `\.      |    ,8
       `7.   '. ,/
          `\. |/
             `3
                `\.
                   ` w
    """
    # from http://pages.ripco.net/~jgamble/nw.html:
    # swap(0, 1);
    # swap(2, 3);
    # swap(0, 2);
    # swap(1, 3);
    # swap(1, 2);
    #
    # You can determine the edge swaps (a,b) by asking
    # 'Via which edge can I get from a to b?'
    #
    # e.g. swap(0,2):
    # path 1) 0 -- 7 -- (3) -- 9 -- 2 |--> swap(7,9)
    # path 2) 0 -- 4 -- (1) -- 5 -- 2 |--> swap(4,5)
    #
    # Each _swap step produces a valid Tet10.


    if n[0] > n[1]:
        swap(n, 0, 1)
        swap(n, 5, 6)
        swap(n, 7, 8)

    if n[2] > n[3]:
        swap(n, 2, 3)
        swap(n, 6, 7)
        swap(n, 5, 8)

    if n[0] > n[2]:
        swap(n, 0, 2)
        swap(n, 7, 9)
        swap(n, 4, 5)

    if n[1] > n[3]:
        swap(n, 1, 3)
        swap(n, 5, 9)
        swap(n, 4, 7)

    if n[1] > n[2]:
        swap(n, 1, 2)
        swap(n, 8, 9)
        swap(n, 4, 6)


def triangle6(n, swap):
    r"""
    Reorder the vertex nodes so that n[0] < n[1] < n[2].
    The order of the edge nodes n[3:6] is changed such that the cells
    still form a valid Triangle6.

    Triangle6:

    v
    ^
    |
    2
    |`\
    |  `\
    5    `4
    |      `\
    |        `\
    0-----3----1 --> u
    """

    # from http://pages.ripco.net/~jgamble/nw.html:
    # swap(1, 2);
    # swap(0, 2);
    # swap(0, 1);
    # Each _swap step produces a valid Triangle6.

    if n[1] > n[2]:
        swap(n, 1, 2)
        swap(n, 3, 5)

    if n[0] > n[2]:
        swap(n, 0, 2)
        swap(n, 3, 4)

    if n[0] > n[1]:
        swap(n, 0, 1)
        swap(n, 4, 5)


