def get_r_dependence(ts, coors, mode=None, **kwargs):
    """
    We want to add an r factor to the laplacian integral.

    For scalar parameters, the shape has to be set to `(coors.shape[0], 1, 1)`.
    """
    if mode == 'qp':
        x = coors[:,1]
        val = x.copy()
        val.shape = (coors.shape[0], 1, 1)
        return {'val' : val}

filename_mesh = 'gabe2_openclosed.msh'
#filename_mesh = 'tmp/mesh.vtk'

options = {
    'save_eig_vectors' : None,
    'eigen_solver' : 'eigen1',
    'n_eigs':12,
    'evps': 'eig',
}

# Whole domain $Y$.
region_1 = {
    'name' : 'Omega',
    'select' : 'all',
}

functions = {
    'get_r_dependence' : (get_r_dependence,),
}

material_1 = {
    'name' : 'm',
    'function' : 'get_r_dependence',
}

field_0 = {
    'name' : 'field_Psi',
    'dtype' : 'real',
    'shape' : 'scalar',
    'region' : 'Omega',
    'approx_order' : 1,
}

integral_1 = {
    'name' : 'i1',
    'order' : 2,
}

variable_1 = {
    'name' : 'Psi',
    'kind' : 'unknown field',
    'field' : 'field_Psi',
    'order' : 0,
}
variable_2 = {
    'name' : 'v',
    'kind' : 'test field',
    'field' : 'field_Psi',
    'dual' : 'Psi',
}

ebcs = {}

equations = {
    'lhs' : """  dw_laplace.i1.Omega( m.val, v, Psi )""",
    'rhs' : """dw_volume_dot.i1.Omega( m.val, v, Psi )""",
}

solver_1 = {
    'name' : 'eigen1',
    'kind' : 'eig.scipy',
    'method' : 'eigh',
    'which' : 'LM',
    'sigma' : 0,
}

solvers = {
        'eig' : ('eig.scipy', {
            'method' : 'eigsh',
            'tol' : 1e-10,
            'maxiter' : 150,

            # Compute the eigenvalues near tau using the shift-invert mode.                                                                                                                                         
            'which' : 'LM',
            'sigma' : 0.0,
        }),
    }



