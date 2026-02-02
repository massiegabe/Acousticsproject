#!/usr/bin/env python
"""
Acoustic mode solver

Type:

$ ./acoustics.py

for usage and help.
"""
import os
from optparse import OptionParser

import sfepy
from sfepy.base.conf import ProblemConf, get_standard_keywords
#from acoustics_app import AcousticsApp
from sfepy.applications import EVPSolverApp

def main():
    parser = OptionParser(usage='', version='%prog ' + sfepy.__version__)
    options, args = parser.parse_args()
    options.conf = None
    options.app_options = None
    options.output_filename_trunk = None
    mesh_filename = 'tmp/mesh.vtk'
    filename_in = 'acoustics_prob.py'
    required, other = get_standard_keywords()
    conf = ProblemConf.from_file_and_options(filename_in, options, required, other)
    conf.filename_mesh = mesh_filename
    conf.options.absolute_mesh_path = True
    conf.options.n_eigs = 12
    app = EVPSolverApp(conf, options, '')
    opts = conf.options
    app()

if __name__ == '__main__':
    main()
