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


# ------------------------------------------------------------
# Region selector functions
# ------------------------------------------------------------
def axis_verts(coors, domain=None):
    return np.where(coors[:, 1] < 1e-10)[0]

def open_verts(coors, domain=None):
    return np.where(coors[:, 0] > 0.569)[0]

def wall_verts(coors, domain=None):
    return np.where(coors[:, 1] > 0.0349)[0]

def closed_verts(coors, domain=None):
    return np.where(coors[:, 0] < 1e-10)[0]

def baffle_verts(coors, domain=None):
    """
    Select vertical baffle faces.
    MUST match geometry parameters in.geo file.
    """
    lambda_val = 439.73837948/1000     # <-- same as .geo
    xb = 0.75 * 439.73837948/1000  # 3/2 lambda location
    t = 50.125/2   /1000           # thickness
    y_gap = 15 /1000   # opening height

    return np.where(
        (coors[:, 0] > xb - t/2 - 1e-4) &
        (coors[:, 0] < xb + t/2 + 1e-4) &
        (coors[:, 1] > y_gap)
    )[0]


# ------------------------------------------------------------
# Mesh file
# ------------------------------------------------------------
filename_mesh = 'new_tube19.mesh'
"filename_mesh = 'new_tube_2d.mesh'"


# ------------------------------------------------------------
# Options
# ------------------------------------------------------------
options = {
    'evps': 'eig',
    'n_eigs': 12,
    'post_process_hook_final': 'print_frequencies',
}


# ------------------------------------------------------------
# Regions
# ------------------------------------------------------------
regions = {
    'Omega'  : 'all',
    'Axis'   : 'cells of group 2',
    'Open'   : 'cells of group 3',
    'Wall'   : 'cells of group 4',
    'Closed' : 'cells of group 5',
    'Baffle' : ('vertices by baffle_verts', 'facet'),
}


# ------------------------------------------------------------
# Functions, materials
# ------------------------------------------------------------
functions = {
    'get_r_dependence': (get_r_dependence,),
    'axis_verts':       (axis_verts,),
    'open_verts':       (open_verts,),
    'wall_verts':       (wall_verts,),
    'closed_verts':     (closed_verts,),
    'baffle_verts':     (baffle_verts,),
}

materials = {
    'm': 'get_r_dependence',
}


# ------------------------------------------------------------
# Field
# ------------------------------------------------------------
fields = {
    'pressure': ('real', 'scalar', 'Omega', 1),
}


# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
variables = {
    'Psi': ('unknown field', 'pressure', 0),
    'v': ('test field', 'pressure', 'Psi'),
}


# ------------------------------------------------------------
# Boundary conditions
# ------------------------------------------------------------
# Open end = pressure = 0
# Walls + Baffle = natural Neumann (do nothing)
ebcs = {
    'open_bc': ('Open', {'Psi.0': 0.0}),
}


# ------------------------------------------------------------
# Integral
# ------------------------------------------------------------
integrals = {
    'i': 2,
}


# ------------------------------------------------------------
# Equations
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Solver
# ------------------------------------------------------------
solvers = {

    'eig': ('eig.scipy', {
        'method': 'eigsh',
        'tol': 1e-12,
        'maxiter': 500,
        'which': 'LM',
        'sigma': 0.0,
    }),
}


# ------------------------------------------------------------
# Frequencies
# ------------------------------------------------------------
def print_frequencies(problem, evp=None, **kwargs):

    eigs = evp.eigs

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

    return evp
