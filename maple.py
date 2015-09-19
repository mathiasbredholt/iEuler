# maple parser for mathnotes
from mathlib import *
import re


def parse(input_string):
    return parse_expression(parse_nested(input_string))


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

# def parse_parenths(input_string):
#   iter = re.finditer(r"[()]", input_string)
#     parenths = []
#     par_depths = [0]
#     for a in iter:
#         parenths.append((a.start(), a.group()))
#         if a.group() is '(':
#             par_depths.append(par_depths.last() + 1)
#         else:
#             par_depths.append(par_depths.last() - 1)
#     par_depths.append(0)
#     return (parenths, par_depths)


def parse_expression(expression):
    operators = ['^', '*', '/', '+', '-']
    for op in operators:
        indices = recursive_index(expression, op, op is '^')
        while not indices is -1:
            print("op=" + op)
            index1 = indices.copy()
            index2 = indices.copy()
            index1[len(index1) - 1] -= 1
            index2[len(index2) - 1] += 1
            print("index1=" + str(index1))
            print("index2=" + str(index2))
            value = []
            value.append(get_list_value(expression, index1))
            value.append(get_list_value(expression, index2))
            for i in range(0, 2):
                if type(value[i]) is str:
                    value[i] = get_math_value(value[i])
                elif type(value[i]) is list:
                    value[i] = parse_expression(value[i])
                # else: is operator
            operator = get_operator(op, value[0], value[1])
            if len(indices) is 1:
                expression[0] = operator
                expression.pop()
                expression.pop()
                return expression
            else:
                set_list_value(
                    expression, indices[0:len(indices) - 1], operator)
            indices = recursive_index(expression, op, op is '^')


def get_math_value(value):
    return Number(value)


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
        return input_list[indices[0]]


def set_list_value(input_list, indices, value):
    if len(indices) > 1:
        set_list_value(input_list[indices[0]], indices[1:len(indices)], value)
    else:
        input_list[indices[0]] = value


def recursive_index(input_list, item, rev=False):
    l = input_list.copy()
    if rev:
        l.reverse()
    for i, x in enumerate(l):
        index = (len(l) - 1 - i) if rev else i
        if x is item:
            return [index]
        elif type(x) is list:
            indices = recursive_index(x, item, rev)
            if not indices is -1:
                return [index] + indices
    return -1
