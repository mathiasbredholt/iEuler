# maple parser for mathnotes
import procio
from mathlib import *
import re
from mathparser import *


def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def parse(input_string):
    # print("parse({})".format(input_string))
    x = parse_nested(input_string.strip(' '))
    # print("{} -> {}".format(input_string, x))
    y = parse_expression(x)
    # print("-> {}".format(y))
    return y
    # return parse_expression(parse_nested(input_string.strip(' ')))


def parse_expression(expression):
    if len(expression) is 1:
        if type(expression[0]) is MathOperator:
            return expression
        elif type(expression[0]) is list:
            return parse_expression(expression[0])
        else:
            return get_math_value(expression[0])
    # print("parse_expression({})".format(expression))
    operators = [r'[\^]', r'[*/]', r'[+-]']
    for op in operators:
        # find indices of first operator of given type
        indices, operator = recursive_index(expression, op, op is r'[\^]')
        # print("op={}, indices={}".format(operator, indices))
        while not indices is -1:

            # Indices of elements before and after operator (operands)
            index1 = indices.copy()
            index2 = indices.copy()
            index1[len(index1) - 1] -= 1
            index2[len(index2) - 1] += 1
            # print("index1=" + str(index1))
            # print("index2=" + str(index2))

            # Iterate through the two operands, parsing them according to their
            # type
            value = []
            value.append(get_list_value(expression, index1))
            value.append(get_list_value(expression, index2))
            for i in range(0, 2):
                if type(value[i]) is list:
                    # operand is an uprocessed list, parse recursively
                    value[i] = parse_expression(value[i])
                elif type(value[i]) is str:
                    # operand is an unprocessed string, convert to Mathvalue
                    value[i] = get_math_value(value[i])
                # else: value is an already processed operator

            operator = get_operator(operator, value[0], value[1])
            # print("expression={}".format(expression))
            inner_exp = get_list_value(expression, indices[0:len(indices) - 1])
            # print("inner={}".format(inner_exp))
            inner_exp[indices[-1] - 1:indices[-1] + 2] = [operator]
            # print("inner={}".format(inner_exp))
            set_list_value(expression, indices[0:len(indices) - 1], inner_exp)
            # print("expression={}".format(expression))
            indices[-1] -= 1

            # print(
            # "len={}".format(len(get_list_value(expression, indices[0:len(indices) - 1]))))
            while len(get_list_value(expression, indices[0:len(indices) - 1
                                                         ])) is 1:
                # print("indices={}".format(indices))
                # print("expression={}".format(expression))

                if len(indices) is 1:
                    # operator contains complete expression, return
                    return operator

                # expression in innermost parentheses contains only the parsed
                # operator and its operands. since the sublist only contains
                # operator, replace it with operator
                set_list_value(
                    expression, indices[0:len(indices) - 1], operator)
                # print("expression={}".format(expression))
                indices.pop()

            # find next operator
            indices, operator = recursive_index(expression, op, op is r'[\^]')


def get_math_value(value):
    value = value.strip("")
    if not re.match(r"[^0-9.]+", value) or value is "pi":
        return Number(value)
    else:
        return Variable(value)
    # print("get_math_value({})".format(value))


def get_operator(symbol, value1, value2):
    # print("get_operator({},{},{})".format(symbol, value1, value2))
    if symbol is '^':
        return Power(value1, value2)
    elif symbol is '*':
        return MulOp(value1, value2)
    elif symbol is '/':
        return Fraction(value1, value2)
    elif symbol is '+':
        return AddOp(value1, value2)
    elif symbol is '-':
        return SubOp(value1, value2)


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
