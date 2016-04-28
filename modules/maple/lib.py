import mathlib as ml

functions = {
    "sqrt": {
        "object": lambda x: ml.Root(x, ml.Number("2")),
        "num_args": 1
    },
    "int": {
        "object": ml.Integral,
        "num_args": 2
    },
    "diff": {
        "object": ml.Derivative,
        "num_args": 2
    },
    "__default__": {
        "object": ml.Function,
    }
}

variables = {
    "__default__": {
        "object": ml.Variable
    }
}

special_symbols = {
    'μ': "mu",
    "pi": "Pi",
}

symbols = {
    "__standard__":
    ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
     'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau',
     'upsilon', 'phi', 'chi', 'psi', 'omega', 'Alpha', 'Beta', 'Gamma',
     'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda',
     'Mu', 'Nu', 'Xi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi',
     'Psi', 'Omega', 'nabla', 'infinity', 'partial'],
    "CC": "complexes",
    "RR": "reals",
    "QQ": "rationals",
    "ZZ": "integers",
    "NN": "naturals",
    "AA": "forall",
    "EE": "exists",
    "oo": "infinity",
    "inf": "infinity",
    "grad": "nabla",
    "µ": "mu",
    "Pi": "pi",
    "dd": "partial"
}
