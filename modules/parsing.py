import re
import iEuler.modules.mathlib as ml
from functools import reduce
from iEuler.modules.pyparsing.pyparsing import Keyword, White, NotAny, alphas, alphas8bit, nums, Word


letters = alphas + alphas8bit

chars = letters + nums

space = White(' ')

word = Word(letters, chars)

word_start = NotAny(chars)

word_end = NotAny(chars)

no_white = NotAny(White())


def make_keyword_list(list):
    # ['x', 'y'] -> Keyword('x') | Keyword('y')
    return reduce(lambda x, y: x | y, map(Keyword, list))


def get_value(toks):
    # print("get_value toks: {}".format(toks))
    value = toks[0]
    if value[0] == ".":
        number = ml.Number("0" + value)
    else:
        number = ml.Number(value)
    if len(toks) > 1 and type(toks[1]) in [ml.Function, ml.Unit, ml.Variable]:
        return ml.MulOp(number, toks[1])
    return number


def get_function(toks, functions):
    name = toks[0]
    args = toks[1:]
    if name in functions:
        if "num_args" in functions[name] and functions[name]["num_args"
                                                             ] != len(args):
            # error
            pass
        return functions[name]["object"](*args)
    else:
        return functions["__default__"]["object"](name, *args)


def get_variable(toks, variables, symbols={"__standard__": []}, user_variables={}):
    value = toks[0]
    if len(toks) > 2 and toks[1] == "_":
        if type(toks[2]) is str:
            subscript = ml.Variable(str)
        elif type(toks[2]) is ml.Unit:
            subscript = toks[2].convert_to_variable()
        else:
            subscript = toks[2]
        name = value + "_" + toks[2].name()
    else:
        subscript = None
        name = value

    # print(value)

    # print("Variable: {}".format(name))
    if name in variables:
        return variables[name]["object"]()
    elif value in symbols["__standard__"]:
        return ml.Variable(value, is_symbol=True, subscript=subscript)
    elif value in symbols:
        return ml.Variable(symbols[value], is_symbol=True, subscript=subscript)
    else:
        return variables["__default__"]["object"](value, subscript=subscript)


def get_matrix(toks, delimiters):
    values = [[toks[0]]]
    row = 0
    for i in range(1, len(toks), 2):
        if toks[i] in delimiters["vertical"]:
            row += 1
            values += [[toks[i + 1]]]
        elif toks[i] in delimiters["horizontal"]:
            # print("values: {}, toks[i+1]: {}".format(values, toks[i + 1]))
            values[row] += [toks[i + 1]]
        else:
            # error
            print("invalid delimiter")
    # TODO: Check for irregularity

    return ml.Matrix(values)


def get_ans(toks, workspace):
    print("get_ans>> workspace: {}".format(workspace))
    i = 0
    if len(toks) == 1:
        if workspace["index"] in workspace["parsed_input"].keys():
            if type(workspace["parsed_input"][workspace["index"]]) is ml.Equality:
                eqs = workspace["parsed_input"][workspace["index"]].flatten()
                for x in range(1, len(eqs)):
                    if eqs[x].find(lambda x: type(x) is ml.AnsPlaceholder):
                        return ml.Ans(eqs[x - 1])
            return ml.Ans(ml.Empty())
        else:
            workspace["needs_refresh"] = True
            return ml.AnsPlaceholder()
    else:
        i = int(toks[1])
    if workspace["index"] - i in workspace["parsed_input"].keys():
        value = workspace["parsed_input"][workspace["index"] - i]
    else:
        value = ml.Empty()
    print("get_ans>> value: {}, index: {}".format(value, i))
    return ml.Ans(value, ml.Number(str(i)))
    # return ml.Empty()


def get_unit(toks, units, unknown=False):
    # print("get_unit toks: {}".format(toks))
    if type(toks[0]) is ml.Number:
        return ml.MulOp(toks[0], get_unit(toks[1:], units))
    if len(toks) > 1:
        unit = toks[1]
        prefix = toks[0]
    else:
        unit = toks[0]
        prefix = ""
    if unit in units['aliases']:
        unit = units['aliases'][unit]
    if prefix in units['prefix_aliases']:
        prefix = units['prefix_aliases'][prefix]
    return ml.Unit(unit, prefix, unknown=unknown)


def get_pow_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_pow_op, right=True)
    return ml.Power(value1, value2)


def get_mul_op(toks):
    # print("get_mul_op toks: {}".format(toks))
    value1, value2, op = parse_binary_operator(toks, get_mul_op)
    return ml.MulOp(value1, value2)


def get_cross_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_cross_op)
    return ml.CrossOp(value1, value2)


def get_div_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_div_op)
    return ml.Fraction(value1, value2)


def get_add_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_add_op)
    if op == "+":
        return ml.AddOp(value1, value2)
    else:
        return ml.SubOp(value1, value2)


def get_range_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_range_op)
    return ml.Range(value1, value2)


def get_factorial_op(toks):
    value, op = parse_unary_operator(toks, right=False)
    return ml.Factorial(value)


def get_abs_op(toks):
    return ml.Abs(toks[0])


def get_minus_op(toks):
    # print("get_minus_op toks: {}".format(toks))
    value, op = parse_unary_operator(toks)
    return ml.Minus(value)


def get_equal_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_equal_op)
    return ml.Equality("=", value1, value2)


def parse_binary_operator(toks, func, right=False):
    operator = toks[0][1 if right else -2]
    value1 = toks[0][0 if right else -1]
    if type(value1) is str:
        value1 = get_value(value1)
    if len(toks[0]) > 3:
        value2 = func([toks[0][2:] if right else toks[0][:-2]])
    else:
        value2 = toks[0][2 if right else 0]
        if type(value2) is str:
            value2 = get_value(value2)
    if right:
        return value1, value2, operator
    return value2, value1, operator


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
