# parser for mathnotes default syntax
import mathlib as ml
import mathparser as mp
from parser_mathnotes_lib import *
from functools import reduce
import re
from pyparsing import ParserElement, Regex, Word, Keyword, Literal, White, Group, ZeroOrMore, NotAny, Optional, Forward, Suppress, Combine, oneOf, infixNotation, opAssoc, delimitedList, nums, alphas, printables, alphanums, alphas8bit
import os
import parser_maple
import frink
import latex
import cmdmath
import procio
import tools_plot2d as plot2d
import json


ParserElement.enablePackrat()  # Vastly improves pyparsing performance


####################################################
# GENERATE MATHNOTES STRING FROM MATHLIB OPERATORS #
####################################################

def generate(input_expr):
    return convert_expr(input_expr)


def convert_expr(input_expr):
    return input_expr.to_maple()


def parentheses(input_expr, do=True):
    if not type(input_expr) is str:
        input_expr = convert_expr(input_expr)
    if do:
        return "( {} )".format(input_expr)
    return input_expr


def convert_value(self):
    return self.value


def convert_minus(self):
    return "-{}".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_factorial(self):
    return "{}!".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    output = "{} {}"
    num_after = type(self.value2) is ml.Number or type(self.value2) in [
        ml.MulOp, ml.Power
    ] and type(self.value2.get_first()) is ml.Number
    if num_after:
        output = "{} * {}"
    if type(self.value1) in [ml.AddOp, ml.SubOp]:
        output_1 = parentheses(self.value1)
    else:
        output_1 = convert_expr(self.value1)
    if type(self.value2) in [ml.AddOp, ml.SubOp]:
        output_2 = parentheses(self.value2)
    else:
        output_2 = convert_expr(self.value2)
    return output.format(output_1, output_2)


def convert_fraction(self):
    return "{}/{} ".format(
        parentheses(self.value1, type(self.value1) in [ml.AddOp, ml.SubOp]),
        parentheses(self.value2,
                    not type(self.value2) in [ml.Number, ml.Variable]))


def convert_power(self):
    if type(self.value1) is ml.Number or\
       type(self.value1) is ml.Variable or\
       type(self.value1) is ml.Root:
        return "{}^({}) ".format(convert_expr(self.value1),
                                 convert_expr(self.value2))
    else:
        return "{}^({}) ".format(parentheses(self.value1),
                                 convert_expr(self.value2))


def convert_root(self):
    if self.value2.get_value() == "2":
        return "sqrt({}) ".format(convert_expr(self.value1))
    else:
        return "root({}, {}) ".format(
            convert_expr(self.value1), convert_expr(self.value2))


def convert_integral(self):
    if self.range_from is None:
        return "int {} d{} ".format(
            convert_expr(self.value), convert_expr(self.variable))
    else:
        return "int from {} to {} d{} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.variable))


def convert_derivative(self):
    if self.nth.get_value == "1":
        return "d{}/d{} ".format(convert_expr(self.value),
                                 convert_expr(self.variable))
    else:
        return "D({})({})({})".format(
            convert_expr(self.nth), convert_expr(self.value),
            convert_expr(self.variable))


def convert_function(self):
    text = self.name
    text += "("
    for i, arg in enumerate(self.value):
        if i != 0:
            text += ", "
        text += convert_expr(arg)
    text += ")"
    return text

# Extending mathlib classes with to_maple method for duck typing
ml.MathValue.to_mathnotes = convert_value
ml.Minus.to_mathnotes = convert_minus
ml.Factorial.to_mathnotes = convert_factorial
ml.AddOp.to_mathnotes = convert_addop
ml.SubOp.to_mathnotes = convert_subop
ml.MulOp.to_mathnotes = convert_mulop
ml.Fraction.to_mathnotes = convert_fraction
ml.Power.to_mathnotes = convert_power
ml.Root.to_mathnotes = convert_root
ml.Integral.to_mathnotes = convert_integral
ml.Derivative.to_mathnotes = convert_derivative
ml.Function.to_mathnotes = convert_function


###############################################
# PARSE MATHNOTES STRING TO MATHLIB OPERATORS #
###############################################

__settings__, maple_proc, frink_proc, gui_mode = [None] * 4


def init():
    global __settings__

    with open('mathnotes.conf', 'r') as f:
        __settings__ = json.load(f)


def parse(input_string):
    x = parse_expression(input_string)
    return x


def make_keyword_list(list):
    # ['x', 'y'] -> Keyword('x') | Keyword('y')
    return reduce(lambda x, y: x | y, map(Keyword, list))


def get_decorator(toks):
    value, op = mp.parse_unary_operator(toks)
    value.add_decorator(op)
    return value


def get_equality_op(toks):
    global maple_proc
    t = toks[0]
    value1, value2, op = mp.parse_binary_operator(toks, get_equality_op)
    hidden = False
    if "equals" in t:
        type = "="
        if t["equals"]["modifier"]:
            if "#" in t["equals"]["modifier"]:
                if maple_proc is None:
                    if not gui_mode:
                        print("Starting Maple...")
                    # Spawn Maple subprocess.
                    # Returns instance of process, queue and thread for
                    # asynchronous I/O
                    maple_proc = parser_maple.init(__settings__["maple"])
                value2 = parser_maple.query(value2, *maple_proc)
            if "::" in t["equals"]["modifier"]:
                hidden = True
            elif ":" in t["equals"]["modifier"]:
                pass
    else:
        type = op[0]

    return ml.Equality(type, value1, value2, hidden)


def make_expression():

    ParserElement.setDefaultWhitespaceChars(' \t')

    deco_kw_list = make_keyword_list(
        ['hat', 'bar', 'ul', 'vec', 'dot', 'ddot', 'tdot'])
    equality_kw_list = make_keyword_list(
        ['in', '!in', 'sub', 'sup', 'sube', 'supe'])
    letters = alphas + alphas8bit + "_"
    chars = letters + nums
    space = White(' ')

    function = Forward()
    expr = Forward()
    number = Combine(Word(nums) + Optional("." + Word(nums)))
    name = NotAny(deco_kw_list | equality_kw_list) + Word(letters, chars)
    variable = name.copy()
    operand = number.setParseAction(mp.get_value) | function.setParseAction(lambda x: mp.get_function(x, functions)) | variable.setParseAction(
        lambda x: mp.get_variable(x, variables))
    function << Combine(name + Suppress("(")) + \
        delimitedList(expr, delim=',') + Suppress(")")

    factop = Literal('!') + space
    signop = space + Literal('-')
    expop = Literal('^')
    fracop = Literal('/')
    multop1 = space.copy()
    multop2 = Literal('*')
    crossop = Keyword('cross')
    plusop = oneOf('+ -')
    equals = Group(Regex(
        r'((?P<modifier>[:#])+(?P<option>[a-zA-Z]*))?=')).setResultsName("equals")
    other_equals = oneOf('== <= >= < >')
    equalop = Group(other_equals) | equals | Group(equality_kw_list)

    right = opAssoc.RIGHT
    left = opAssoc.LEFT
    expr << infixNotation(operand,
                          [
                              (factop,          1, left,    mp.get_factorial_op),
                              (deco_kw_list,    1, right,   get_decorator),
                              (signop,          1, right,   mp.get_minus_op),
                              (expop,           2, right,   mp.get_pow_op),
                              (fracop,          2, left,    mp.get_div_op),
                              (multop1,         2, left,    mp.get_mul_op),
                              (multop2,         2, left,    mp.get_mul_op),
                              (crossop,         2, left,    mp.get_mul_op),
                              (plusop,          2, left,    mp.get_add_op),
                              (equalop,         2, left,    get_equality_op)
                          ]
                          )
    expr.parseWithTabs()
    return expr


expression = make_expression()


def parse(text, gui=False):
    global gui_mode
    gui_mode = gui
    return expression.parseString(text)[0]
