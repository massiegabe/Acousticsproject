Mesh.MshFileVersion = 2.2;

// Geometry parameters
L = 439.73837948;     // tube length (m)
R = (25.4);    // radius (m)
lc = 0.005;   // mesh size

// --- Wavelength ) ---
// Baffle thickness (m)
t = 10; 

// Baffle position (3/2 lambda from left end)
xb = 0.75 * L;

// Baffle vertical extent 
y_gap = (2.86);

// --- Points ---
// Tube corners
Point(1) = {0, 0, 0, lc};
Point(2) = {L, 0, 0, lc};
Point(3) = {L, R, 0, lc};
Point(4) = {0, R, 0, lc};

// Baffle left face
Point(5) = {xb - t/2, R, 0, lc};
Point(6) = {xb - t/2, y_gap, 0, lc};

// Baffle right face
Point(7) = {xb + t/2, R, 0, lc};
Point(8) = {xb + t/2, y_gap, 0, lc};

// Bottom points for splitting
Point(9)  = {xb - t/2, 0, 0, lc};
Point(10) = {xb + t/2, 0, 0, lc};

// --- Lines ---
// Outer boundary
Line(1) = {1,9};
Line(2) = {9,10};
Line(3) = {10,2};
Line(4) = {2,3};
Line(5) = {3,7};
Line(6) = {7,5};
Line(7) = {5,4};
Line(8) = {4,1};

// Baffle interior
Line(9)  = {9,6};
Line(10) = {6,5};
Line(11) = {10,8};
Line(12) = {8,7};
Line(13) = {6,8}; // gap under baffle

// --- Surfaces ---
// Left region
Curve Loop(21) = {1,9,10,7,8};
Plane Surface(21) = {21};

// Baffle region (middle)
Curve Loop(22) = {2,11,-13,-9};
Plane Surface(22) = {22};

// Right region
Curve Loop(23) = {3,4,5,-12,-11};
Plane Surface(23) = {23};

// Physical groups
Physical Surface("Omega") = {21,22,23};

Physical Curve("Axis")   = {1,2,3};
Physical Curve("Open")   = {4};
Physical Curve("Wall")   = {5,6,7};
Physical Curve("Closed") = {8};

// Structured mesh
Transfinite Curve {1,2,3,5,6,7} = 200;
Transfinite Curve {4,8,9,10,11,12,13} = 30;

Transfinite Surface {21};
Transfinite Surface {22};
Transfinite Surface {23};

Recombine Surface {21};
Recombine Surface {22};
Recombine Surface {23};