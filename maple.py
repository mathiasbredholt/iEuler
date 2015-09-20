# maple parser for mathnotes
import procio
from mathlib import *
import re


def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def parse(input_string):
    # x = parse_nested(input_string).copy()
    # print("{} -> {}".format(input_string, x))
    # y = parse_expression(x)
    # print("-> {}".format(y))
    # return y
    return parse_expression(parse_nested(input_string.strip(' ')))


def parse_nested(text, left=r'[(]', right=r'[)]', operators=r'[-+*/^]'):
    """ Based on http://stackoverflow.com/a/17141899/190597 (falsetru) """
    pat = r'({}|{}|{})'.format(left, right, operators)
    tokens = re.split(pat, text)
    stack = [[]]
    for x in tokens:
        # if not x or re.match(sep, x): continue
        if not x:
            continue
        if re.match(left, x):
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif re.match(right, x):
            stack.pop()
            if not stack:
                raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        print(stack)
        raise ValueError('error: closing bracket is missing')
    return stack.pop()


def parse_expression(expression):
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
                if type(value[i]) is str:
                    # operand is an unprocessed string, convert to Mathvalue
                    value[i] = get_math_value(value[i])
                elif type(value[i]) is list:
                    # operand is an uprocessed list, parse recursively
                    value[i] = parse_expression(value[i])
                # else: value is an already processed operator

            operator = get_operator(operator, value[0], value[1])

            while len(get_list_value(expression, indices[0:len(indices) - 1])) in [1, 3]:
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
            else:
                # expression in innermost parentheses contains more unparsed
                # operations, just replace the three items, constituting the
                # parsed operator, with operator
                inner_exp = get_list_value(
                    expression, indices[0:len(indices) - 1])
                inner_exp[indices[-1] - 1:indices[-1] + 2] = [operator]
                set_list_value(
                    expression, indices[0:len(indices) - 1], inner_exp)

            # find next operator
            indices, operator = recursive_index(expression, op, op is r'[\^]')


def get_math_value(value):
    return Number(value.strip(' '))


def get_operator(symbol, value1, value2):
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
    if len(indices) > 1:
        return get_list_value(input_list[indices[0]], indices[1:len(indices)])
    else:
        if not indices:
            # indices is empty
            return input_list
        return input_list[indices[0]]


def set_list_value(input_list, indices, value):
    if len(indices) > 1:
        set_list_value(input_list[indices[0]], indices[1:len(indices)], value)
    else:
        if not indices:
            # indices is empty
            input_list = value
        else:
            input_list[indices[0]] = value


def recursive_index(input_list, regex, rev=False):
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
