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
    indices = recursive_index(expression, "^", True)
    while not indices is -1:
        index1, index2 = indices
        index1[len(index1) - 1] -= 1
        index2[len(index2) - 1] += 1
        set_list_value(a, indices[0:len(indices) - 1], )
        indices = recursive_index(expression, "^", True)


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
