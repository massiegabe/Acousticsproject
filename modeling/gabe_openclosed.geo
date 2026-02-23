L = 0.57;
R = 0.035;

// Mesh resolution
lc = 0.01;

// Geometry
Point(1) = {0, -R, 0, lc};
Point(2) = {L, -R, 0, lc};
Point(3) = {L,  R, 0, lc};
Point(4) = {0,  R, 0, lc};

Line(1) = {1,2}; // bottom wall
Line(2) = {2,3}; // OPEN end
Line(3) = {3,4}; // top wall
Line(4) = {4,1}; // CLOSED end

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

Physical Surface("air") = {1};

Physical Curve("open") = {2};
Physical Curve("closed") = {4};
Physical Curve("walls") = {1,3};

Transfinite Curve {1,3} = 120;
Transfinite Curve {2,4} = 20;
Transfinite Surface {1};
Recombine Surface {1};