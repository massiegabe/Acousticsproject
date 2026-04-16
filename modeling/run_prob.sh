#!/usr/bin/env bash

gmsh long_tube_wm.geo long_tube_wm.msh 
python ./convert_mesh_2d.py long_tube_wm.msh long_tube_wm.mesh
sfepy-run acoustics_prob_openclosed.py

