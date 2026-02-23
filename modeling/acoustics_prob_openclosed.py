import numpy as np
# ------------------------------------------------------------
# Speed of sound (m/s)
# ------------------------------------------------------------
c_sound = 343.0


# r dependence
def get_r_dependence(ts, coors, mode=None, **kwargs):
    """
    Axisymmetric correction: multiply integrals by r.
    coors[:,1] is the radial coordinate.
    """
    if mode == 'qp':
        r = coors[:, 1]
        val = r.copy()
        val.shape = (coors.shape[0], 1, 1)
        return {'val': val}


# Mesh file
filename_mesh = 'gabe2_openclosed.msh'


# Options
options = {
    'save_eig_vectors': True,
    'eigen_solver': 'eig',
    'n_eigs': 12,
    'post_process_hook': 'print_frequencies',
}

# Regions
regions = {
    'Omega'  : 'all',

    'Axis'   : ('vertices of group 2',),
    'Open'   : ('vertices of group 3',),
    'Wall'   : ('vertices of group 4',),
    'Closed' : ('vertices of group 5',),
}

# Functions,materials
functions = {
    'get_r_dependence': (get_r_dependence,),
}

materials = {
    'm': 'get_r_dependence',
}


# Field
fields = {
    'pressure': ('real', 'scalar', 'Omega', 1),
}


# Variables
variables = {
    'Psi': ('unknown field', 'pressure', 0),
    'v': ('test field', 'pressure', 'Psi'),
}


# Boundary conditions
# Open end = pressure = 0
# Closed end = natural Neumann
ebcs = {
    'open_bc': ('Open', {'Psi.0': 0.0}),
}


# Integral
integrals = {
    'i': 2,
}


# Equations
equations = {

    'lhs':
    """
    dw_laplace.i.Omega(m.val, v, Psi)
    """,

    'rhs':
    """
    dw_volume_dot.i.Omega(m.val, v, Psi)
    """,
}


# Solver
solvers = {

    'eig': ('eig.scipy', {
        'method': 'eigsh',
        'tol': 1e-12,
        'maxiter': 500,
        'which': 'LM',
        'sigma': 0.0,
    }),
}


# Frequencies
def print_frequencies(problem, evp_results, state=None, extend=False):

    eigs = evp_results.eigs

    print("\n====================================")
    print("Eigenvalues and Frequencies")
    print("====================================\n")

    print("Mode    Eigenvalue        Frequency (Hz)")
    print("----------------------------------------")

    for i, eig in enumerate(eigs):

        if eig < 0:
            freq = 0.0
        else:
            freq = (c_sound / (2*np.pi)) * np.sqrt(eig)

        print(f"{i+1:4d}   {eig:12.6e}   {freq:10.3f}")

    print("\n====================================\n")

    return state