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
    "plot": {
        "object": ml.Plot,
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
