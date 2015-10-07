
import re
from mathlib import *
from pyparsing import ParserElement, Word, Literal, ZeroOrMore, Optional, Forward, Suppress, Combine, oneOf, infixNotation, opAssoc, nums, alphas

ParserElement.enablePackrat()


def make_expression():
    function = Forward()
    expression = Forward()
    number = Combine(Word(nums) + Optional("." + Word(nums)))
    variable = Word(alphas)
    operand = number.setParseAction(get_value) | function.setParseAction(get_function) | variable.setParseAction(
        get_variable)
    function << Combine(Word(alphas) + Suppress("(")) + expression + \
        ZeroOrMore(Suppress(",") + expression) + Suppress(")")

    expop = Literal('^')
    signop = Literal('-')
    fracop = Literal('/')
    multop = Literal('*')
    plusop = oneOf('+ -')
    factop = Literal('!')

    expression << infixNotation(operand,
                                [(factop, 1, opAssoc.LEFT,
                                  lambda x: get_unary_operator(x, right=False)),
                                 (signop, 1, opAssoc.RIGHT,
                                  lambda x: get_unary_operator(x, right=True)),
                                 (expop, 2, opAssoc.RIGHT, get_binary_operator),
                                 (fracop, 2, opAssoc.LEFT, get_binary_operator),
                                 (multop, 2, opAssoc.LEFT, get_binary_operator),
                                 (plusop, 2, opAssoc.LEFT, get_binary_operator)]
                                )
    return expression


def parse_expression(text):
    return expression.parseString(text)[0]


def get_function(toks):
    # print("toks={}".format(toks))
    name = toks[0]
    args = toks[1:]
    if name == "sqrt":
        return Root(args[0], Number("2"))
    elif name == "int":
        return Integral(args[0], args[1])
    elif name == "diff":
        return Derivative(args[0], args[1])
    else:
        return Function(name, args)


def get_value(toks):
    value = toks[0]
    # print("Value: {}".format(value))
    return Number(value)


def get_variable(toks):
    name = toks[0]
    # print("Variable: {}".format(name))
    if name == "pi":
        return Number(name)
    return Variable(name)


def get_binary_operator(toks):
    operator = toks[0][1]
    # print("Operator: {}".format(operator))
    value1 = toks[0][0]
    if type(value1) is str:
        value1 = get_value(value1)
    if len(toks[0]) > 3:
        value2 = get_binary_operator([toks[0][2:]])
    else:
        value2 = toks[0][2]
        if type(value2) is str:
            value2 = get_value(value2)
    # print("    value1: {}, value2: {}".format(value1, value2))
    if operator == '^':
        return Power(value1, value2)
    elif operator == '*':
        return MulOp(value1, value2)
    elif operator == '/':
        return Fraction(value1, value2)
    elif operator == '+':
        return AddOp(value1, value2)
    elif operator == '-':
        return SubOp(value1, value2)


def get_unary_operator(toks, right=True):
    operator = toks[0][0 if right else -1]
    # print("Operator: {}".format(operator))
    if len(toks[0]) > 2:
        value = get_unary_operator([toks[0][1:] if right else toks[0][:-1]])
    else:
        value = toks[0][1 if right else 0]
        if type(value) is str:
            value = get_value(value)
    # print("    value: {}".format(value))
    if operator == '!':
        return Factorial(value)
    elif operator == '-':
        return Minus(value)

expression = make_expression()

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
