def tet10(data):
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

    n_swaps = 0
    for n in data:
        if n[0] > n[1]:
            n[0], n[1] = n[1], n[0]
            n[5], n[6] = n[6], n[5]
            n[8], n[7] = n[7], n[8]
            n_swaps += 3

        if n[2] > n[3]:
            n[2], n[3] = n[3], n[2]
            n[6], n[7] = n[7], n[6]
            n[5], n[8] = n[8], n[5]
            n_swaps += 3

        if n[0] > n[2]:
            n[0], n[2] = n[2], n[0]
            n[7], n[9] = n[9], n[7]
            n[4], n[5] = n[5], n[4]
            n_swaps += 3

        if n[1] > n[3]:
            n[1], n[3] = n[3], n[1]
            n[5], n[9] = n[9], n[5]
            n[4], n[7] = n[7], n[4]
            n_swaps += 3

        if n[1] > n[2]:
            n[1], n[2] = n[2], n[1]
            n[8], n[9] = n[9], n[8]
            n[4], n[6] = n[6], n[4]
            n_swaps += 3
    return n_swaps


def triangle6(data):
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

    n_swaps = 0
    for n in data:
        if n[1] > n[2]:
            n[1], n[2] = n[2], n[1]
            n[3], n[5] = n[5], n[3]
            n_swaps += 2

        if n[0] > n[2]:
            n[0], n[2] = n[2], n[0]
            n[3], n[4] = n[4], n[3]
            n_swaps += 2

        if n[0] > n[1]:
            n[0], n[1] = n[1], n[0]
            n[4], n[5] = n[5], n[4]
            n_swaps += 2
    return n_swaps
