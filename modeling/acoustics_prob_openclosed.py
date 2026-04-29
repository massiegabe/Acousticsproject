import numpy as np
# ------------------------------------------------------------
# Speed of sound (m/s) — mesh is in metres
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


# Region selector functions — coordinates are in metres.
# Geometry (from long_tube_wm.geo, converted mm→m):
#   half-length  l = 0.2955 m  (x from -0.2955 to +0.2955)
#   outer radius r = 0.02615 m
#   baffle inner a = 0.011925 m  at x = ±0.005963 m

def axis_verts(coors, domain=None):
    """Bottom edge: y = 0 (axis of symmetry)."""
    return np.where(coors[:, 1] < 1e-6)[0]

def open_verts(coors, domain=None):
    """Right face: x ≈ +0.2955 m (pressure-release open end)."""
    return np.where(coors[:, 0] > 0.294)[0]

def wall_verts(coors, domain=None):
    """Outer wall and baffle surfaces (rigid, Neumann — natural BC)."""
    top  = coors[:, 1] > 0.025                      # outer wall y ≈ 0.02615
    baf  = (np.abs(coors[:, 0]) < 0.007) & (coors[:, 1] > 0.011)  # baffle faces
    return np.where(top | baf)[0]

def closed_verts(coors, domain=None):
    """Left face: x ≈ -0.2955 m (rigid closed end — natural BC)."""
    return np.where(coors[:, 0] < -0.294)[0]


# Mesh file
filename_mesh = 'long_tube_wm.mesh'


# Options
options = {
    'evps': 'eig',
    'n_eigs': 12,
    'post_process_hook_final': 'print_frequencies',
}

# Regions — inline coordinate expressions (mesh is in metres after mm→m conversion).
# Geometry:  x in [-0.2955, +0.2955],  y in [0, 0.02615]
# Boundary regions must use the ('select', 'facet') tuple form so sfepy
# creates a facet-kind region rather than trying to find complete cells.
regions = {
    'Omega'  : 'all',
    'Axis'   : ('vertices in (y < 1e-6)',    'facet'),  # y = 0  (axis of symmetry)
    'Open'   : ('vertices in (x > 0.294)',   'facet'),  # x ≈ +0.2955  (open end)
    'Wall'   : ('vertices in (y > 0.025)',   'facet'),  # y ≈ 0.02615  (outer wall)
    'Closed' : ('vertices in (x < -0.294)', 'facet'),  # x ≈ -0.2955  (closed end)
}

# Functions, materials
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
# Open end = pressure = 0 (pressure-release)
# Closed end + walls = natural Neumann (zero normal velocity)
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
