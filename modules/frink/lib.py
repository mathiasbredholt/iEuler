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
    "pi": {
        "object": lambda: ml.Number("pi")
    },
    "__default__": {
        "object": ml.Variable
    }
}

units = {
    'units': ['V', 'A', 'J', 'm', 's', 'K', 'W', 'H', 'F', 'T', 'g', 'Hz', 'N', 'Pa', 'C', 'Ohm', 'ohm', 'Omega', 'S', 'Wb', 'lm', 'lx', 'Bq', 'Gy', 'Sv', 'cd', 'mol'],
    'aliases': {},
    'plural': 's',
    'prefixes': {'y': -24, 'z': -21, 'a': -18, 'f': -15, 'p': -12, 'n': -9, u'μ': -6, 'm': -3, 'c': -2, 'd': -1, 'da': 1, 'h': 2, 'k': 3, 'M': 6, 'G': 9, 'T': 12, 'P': 15, 'E': 18, 'Z': 21, 'Y': 24},
    'prefix_aliases': {},
    'escape_character': ''
}

symbols = {
    "__standard__":
    ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
     'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau',
     'upsilon', 'phi', 'chi', 'psi', 'omega', 'Alpha', 'Beta', 'Gamma',
     'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda',
     'Mu', 'Nu', 'Xi', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi',
     'Psi', 'Omega'],
}
