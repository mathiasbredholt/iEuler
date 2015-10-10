
import re
import mathlib as ml


def get_value(toks):
    value = toks[0]
    # print("Value: {}".format(value))
    return ml.Number(value)


def get_function(toks, functions):
    name = toks[0]
    args = toks[1:]
    if name in functions:
        if "num_args" in functions[name] and functions[name]["num_args"] != len(args):
            # error
            pass
        return functions[name]["object"](*args)
    else:
        return functions["__default__"]["object"](name, *args)


def get_variable(toks, variables):
    name = toks[0]
    # print("Variable: {}".format(name))
    if name in variables:
        return variables[name]["object"]()
    else:
        return variables["__default__"]["object"](name)


def get_pow_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_pow_op)
    return ml.Power(value1, value2)


def get_mul_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_mul_op)
    return ml.MulOp(value1, value2)


def get_div_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_div_op)
    return ml.Fraction(value1, value2)


def get_add_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_add_op)
    if op == "+":
        return ml.AddOp(value1, value2)
    else:
        return ml.SubOp(value1, value2)


def get_factorial_op(toks):
    value, op = parse_unary_operator(toks, right=False)
    return ml.Factorial(value)


def get_minus_op(toks):
    value, op = parse_unary_operator(toks)
    return ml.Minus(value)


def parse_binary_operator(toks, func):
    operator = toks[0][1]
    value1 = toks[0][0]
    if type(value1) is str:
        value1 = get_value(value1)
    if len(toks[0]) > 3:
        value2 = func([toks[0][2:]])
    else:
        value2 = toks[0][2]
        if type(value2) is str:
            value2 = get_value(value2)
    return value1, value2, operator


def parse_unary_operator(toks, right=True):
    operator = toks[0][0 if right else -1]
    value = toks[0][1 if right else 0]
    if type(value) is str:
        value = get_value(value)
    return value, operator


# General functions for jagged multidimensinsional lists


def get_list_value(input_list, indices):
    # print("get_list_value({},{})".format(input_list, indices))
    if len(indices) > 1:
        return get_list_value(input_list[indices[0]], indices[1:len(indices)])
    else:
        if not indices:
            # indices is empty
            return input_list
        return input_list[indices[0]]


def set_list_value(input_list, indices, value):
    # print("set_list_value({},{},{})".format(input_list, indices, value))
    if len(indices) > 1:
        set_list_value(input_list[indices[0]], indices[1:len(indices)], value)
    else:
        if not indices:
            # indices is empty
            input_list = value
        else:
            input_list[indices[0]] = value


def recursive_index(input_list, regex, rev=False):
    # print("recursive_index({},{},{})".format(input_list, regex, rev))
    l = input_list.copy()
    if rev:
        l.reverse()
    for i, x in enumerate(l):
        index = (len(l) - 1 - i) if rev else i
        # print("index = {}, x = {}, regex = {}".format(index, x, regex))
        if type(x) is str:
            if re.match(regex, x):
                return ([index], x)
        elif type(x) is list:
            indices, match = recursive_index(x, regex, rev)
            if not indices is -1:
                return ([index] + indices, match)
    return (-1, regex)
