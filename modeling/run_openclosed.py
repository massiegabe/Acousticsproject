#!/usr/bin/env python
"""
Runner for acoustic eigenvalue problem (open-closed tube).

Usage:
    python run_openclosed.py
"""
from sfepy.base.conf import ProblemConf, get_standard_keywords
from sfepy.applications import EVPSolverApp

class Options:
    conf = None
    app_options = None
    output_filename_trunk = None

def main():
    filename_in = 'acoustics_prob_openclosed.py'
    options = Options()

    required, other = get_standard_keywords()
    conf = ProblemConf.from_file_and_options(filename_in, options, required, other)

    app = EVPSolverApp(conf, options, 'acoustics')
    app()

if __name__ == '__main__':
    main()
