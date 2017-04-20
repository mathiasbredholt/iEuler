import iEuler.modules.mathlib as ml

text_fields = '_'

decorator_keywords = ['hat', 'bar', 'ul', 'vec', 'dot', 'ddot', 'tdot',
                      'arrow', 'arr']

equality_keywords = ['in', '!in', 'sub', 'sup', 'sube', 'supe']

units = {
    'units': ['V', 'A', 'J', 'm', 's', 'K', 'W', 'H', 'F', 'T', 'g', 'Hz', 'N', 'Pa', 'C', 'Ohm', 'ohm', 'Omega', 'S', 'Wb', 'lm', 'lx', 'Bq', 'Gy', 'Sv', 'cd', 'mol'],
    'aliases': {
        'volt': 'V',
        'ampere': 'A',
        'amp': 'A',
        'joule': 'J',
        'meter': 'm',
        'second': 's',
        'kelvin': 'K',
        'watt': 'W',
        'henry': 'H',
        'farad': 'F',
        'tesla': 'T',
        'gram': 'g',
        'herz': 'Hz',
        'newton': 'N',
        'pascal': 'Pa',
        'coulomb': 'C',
        'ohm': 'Ohm',
        'Omega': 'Ohm',
        'siemens': 'S',
        'weber': 'Wb',
        'lumen': 'lm',
        'lux': 'lx',
        'bequerel': 'Bq',
        'gray': 'Gy',
        'sievert': 'Sv',
        'candela': 'cd',
        'mole': 'mol'
    },
    'plural': 's',
    'prefixes': ['y', 'z', 'a', 'f', 'p', 'n', u'μ', 'm', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'],
    'prefix_aliases': {
        'yocto': 'y',
        'zepto': 'z',
        'atto': 'a',
        'femto': 'f',
        'pico': 'p',
        'nano': 'n',
        'micro': u'μ',
        'u': u'μ',
        'milli': 'm',
        'centi': 'c',
        'deci': 'd',
        'deca': 'da',
        'hepto': 'h',
        'kilo': 'k',
        'mega': 'M',
        'giga': 'G',
        'tera': 'T',
        'peta': 'P',
        'exa': 'E',
        'zetta': 'Z',
        'yotta': 'Y'
    },
    'escape_character': '.'
}

for key, val in units['aliases'].copy().items():
    units['aliases'][key + units['plural']] = units['aliases'][key]

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
    "sum": {
        "object": ml.Sum,
        "num_args": 2
    },
    "lim": {
        "object": ml.Limit,
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
