Mesh.MshFileVersion = 2.2;

// Geometry parameters
L = 0.57;     // length (m)
R = 0.035;    // radius (m)
lc = 0.005;   // mesh size

// Points
Point(1) = {0, 0, 0, lc};
Point(2) = {L, 0, 0, lc};
Point(3) = {L, R, 0, lc};
Point(4) = {0, R, 0, lc};

// Lines
Line(1) = {1,2}; // axis
Line(2) = {2,3}; // open end
Line(3) = {3,4}; // wall
Line(4) = {4,1}; // closed end

// Surface
Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

Physical Surface("Omega") = {1};

Physical Curve("Axis")   = {1};
Physical Curve("Open")   = {2};
Physical Curve("Wall")   = {3};
Physical Curve("Closed") = {4};

Transfinite Curve {1,3} = 200;
Transfinite Curve {2,4} = 30;
Transfinite Surface {1};
Recombine Surface {1};