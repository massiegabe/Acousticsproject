cl1 = 1;

l=59.10/2.0;
r=52.3;

Point(1) = {-l, 0, 0, cl1};
Point(2) = {-l, r, 0, cl1};
Point(7) = {l, r, 0, cl1};
Point(8) = {l, 0, 0, cl1};
Line(1) = {1, 2};
Line(2) = {2, 7};
Line(7) = {7, 8};
Line(8) = {8, 1};
Line Loop(13) = {1,2,7,8};
Plane Surface(13) = {13};
Physical Surface(19) = {13};
