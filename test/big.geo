SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
Physical Volume(1) = {1};
N = 50;
Transfinite Line {12, 3, 11, 7, 8, 6, 2, 4, 9, 1, 10, 5} = N Using Progression 1;
