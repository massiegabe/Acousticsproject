cl1 = 8;
cl2 = .4;

a=16.9/2.0;
r=52.3/2.0;

t=9.4;

l1 = 290.8 + t/2;
l2 = 290.8 + t/2;

Point(1) = {-l1, 0, 0, cl2};
Point(2) = {-l1, r, 0, cl1};
Point(3) = {-t/2, r, 0, cl2};
Point(4) = {-t/2, a, 0, cl2};
Point(5) = {t/2, a, 0, cl2};
Point(6) = {t/2, r, 0, cl2};
Point(7) = {l2, r, 0, cl1};
Point(8) = {l2, 0, 0, cl2};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 1};
Line(10) = {5, 8};
Line(11) = {4, 1};
Line Loop(13) = {6, 7, -10, 5};
Line Loop(15) = {10, 8, -11, 4};
Line Loop(17) = {11, 1, 2, 3};
Plane Surface(13) = {13};
Plane Surface(15) = {15};
Plane Surface(17) = {17};
Physical Surface(19) = {13,15,17};
