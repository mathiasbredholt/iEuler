import mathlib as ml

text_fields = '_'

decorator_keywords = ['hat', 'bar', 'ul', 'vec', 'dot', 'ddot', 'tdot',
                      'arrow', 'arr']

equality_keywords = ['in', '!in', 'sub', 'sup', 'sube', 'supe']

units = ['V', 'A', 'J', 'm', 's', 'K', 'W', 'H', 'F', 'T', 'g', 'Hz', 'N',
         'Pa', 'C', 'Ohm', 'S', 'Wb', 'lm', 'lx', 'Bq', 'Gy', 'Sv', 'cd', 'mol'
         ]

unit_prefixes = ['y', 'z', 'a', 'f', 'p', 'n', 'μ', 'm', 'c', 'd', 'da', 'h',
                 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

unit_escape_character = '.'

matrix_delimiters = {
    "start": ['<', '['],
    "end": ['>', ']'],
    "horizontal": [',', '\t'],
    "vertical": [';', '\n']
}

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
    "plot": {
        "object": ml.Plot,
        "num_args": 2
    },
    "__default__": {
        "object": ml.Function,
    }
}

variables = {"__default__": {"object": ml.Variable}}

symbols = {
    "__standard__":
    ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
     'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau',
     'upsilon', 'phi', 'chi', 'psi', 'omega', 'Alpha', 'Beta', 'Gamma',
     'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda',
     'Mu', 'Nu', 'Xi', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi',
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
    "dd": "partial"
}
