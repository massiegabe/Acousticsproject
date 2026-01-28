import os
import time
from math import pi

import numpy as nm

from sfepy.base.base import Struct, output, get_default
#from sfepy.applications import PDESolverApp
from sfepy.applications import EVPSolverApp
from sfepy.solvers import Solver

class AcousticsApp(EVPSolverApp):
    """
    Base application for acoustic interior mode calculations.

    Subclasses should typically override `solve_eigen_problem()` method.
    """

    @staticmethod
    def process_options(options):
        """
        Application options setup. Sets default values for missing
        non-compulsory options.

        Options:

        save_eig_vectors : (from_largest, from_smallest) or None
            If None, save all.
        """

        get = options.get
        n_eigs=get('n_eigs', 8)
        return Struct(eigen_solver=get('eigen_solver', None,
                                       'missing "eigen_solver" in options!'),
                      n_eigs=n_eigs,
                      save_eig_vectors=get('save_eig_vectors', None))

    def __init__(self, conf, options, output_prefix, **kwargs):
        EVPSolverApp.__init__(self, conf, options, output_prefix,
                              init_equations=False)

    def setup_options(self):
        EVPSolverApp.setup_options(self)
        opts = AcousticsApp.process_options(self.conf.options)

        self.app_options += opts

    def setup_output(self):
        """
        Setup various file names for the output directory given by
        `self.problem.output_dir`.
        """
        output_dir = self.problem.output_dir

        opts = self.app_options
        opts.output_dir = output_dir
        self.mesh_results_name = os.path.join(opts.output_dir,
                                              self.problem.get_output_name())
        self.eig_results_name = os.path.join(opts.output_dir,
                                             self.problem.ofn_trunk
                                             + '_eigs.txt')

    def call(self):
        # This cannot be in __init__(), as parametric calls may change
        # the output directory.
        self.setup_output()

        evp = self.solve_eigen_problem()

        output("solution saved to %s" % self.problem.get_output_name())
        output("in %s" % self.app_options.output_dir)

        if self.post_process_hook_final is not None: # User postprocessing.
            self.post_process_hook_final(self.problem, evp=evp)

        return evp

    def solve_eigen_problem(self):
        options = self.options
        opts = self.app_options
        pb = self.problem

        dim = pb.domain.mesh.dim

        pb.set_equations(pb.conf.equations)
        pb.time_update()

        output('assembling lhs...')
        tt = time.perf_counter()
        mtx_a = pb.evaluate(pb.conf.equations['lhs'], mode='weak',
                            auto_init=True, dw_mode='matrix')
        output('...done in %.2f s' % (time.perf_counter() - tt))

        output('assembling rhs...')
        tt = time.perf_counter()
        mtx_b = pb.evaluate(pb.conf.equations['rhs'], mode='weak',
                            dw_mode='matrix')
        output('...done in %.2f s' % (time.perf_counter() - tt))

        n_eigs = get_default(opts.n_eigs, mtx_a.shape[0])

        output('computing resonance frequencies...')

        eig = Solver.any_from_conf(pb.get_solver_conf(opts.eigen_solver))
        eigs, mtx_s_phi = eig(mtx_a, mtx_b, n_eigs, eigenvectors=True)

        output('...done')
        for eig in eigs:
            output(eig)

        mtx_phi = self.make_full(mtx_s_phi)

        self.save_results(eigs, mtx_phi)
        return Struct(pb=pb, eigs=eigs, mtx_phi=mtx_phi)

    def make_full(self, mtx_s_phi):
        variables = self.problem.get_variables()

        mtx_phi = nm.empty((variables.di.ptr[-1], mtx_s_phi.shape[1]),
                           dtype=nm.float64)
        for ii in range(mtx_s_phi.shape[1]):
            mtx_phi[:,ii] = variables.make_full_vec(mtx_s_phi[:,ii])

        return mtx_phi

    def save_results_orig(self, eigs, mtx_phi, out=None,
                     mesh_results_name=None, eig_results_name=None):

        mesh_results_name = get_default(mesh_results_name,
                                        self.mesh_results_name)

        eig_results_name = get_default(eig_results_name,
                                       self.eig_results_name)

        pb = self.problem

        save = self.app_options.save_eig_vectors
        n_eigs = self.app_options.n_eigs
        out = get_default(out, {})
        state = pb.create_state()
        for ii in range(eigs.shape[0]):
            if save is not None:
                if (ii > save[0]) and (ii < (n_eigs - save[1])): continue
            state.set_full(mtx_phi[:,ii])
            aux = state.create_output_dict()
            key = aux.keys()[0]
            out[key+'%03d' % ii] = aux[key]

        pb.save_state(mesh_results_name, out=out)

    def save_results(self, eigs, mtx_phi, out=None,
                     mesh_results_name=None, eig_results_name=None):
        mesh_results_name = get_default(mesh_results_name,
                                        self.mesh_results_name)
        eig_results_name = get_default(eig_results_name,
                                       self.eig_results_name)
        pb = self.problem

        save = self.app_options.save_eig_vectors
        n_eigs = self.app_options.n_eigs
        out = get_default(out, {})
        state = pb.create_state()
        aux = {}
        for ii in range(eigs.shape[0]):
            if save is not None:
                if (ii > save[0]) and (ii < (n_eigs - save[1])): continue
            state.set_full(mtx_phi[:,ii])
            aux = state.create_output_dict()
            key = list(aux.keys())[0]
            out[key+'%03d' % ii] = aux[key]

        if aux.get('__mesh__') is not None:
            out['__mesh__'] = aux['__mesh__']

        pb.save_state(mesh_results_name, out=out)

        fd = open(eig_results_name, 'w')
        eigs.tofile(fd, ' ')
        fd.close()

