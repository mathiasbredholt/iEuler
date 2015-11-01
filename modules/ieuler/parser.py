
import mathlib as ml
import parsing as parsing
from modules.ieuler.lib import *
from functools import reduce
import re
from pyparsing import *
import modules.maple.process as mProcess
import modules.tools.plot2d as plot2d
import json

ParserElement.enablePackrat()  # Vastly improves pyparsing performance

__settings__ = None


def init():
    global __settings__

    with open('settings.conf', 'r') as f:
        __settings__ = json.load(f)


def parse(input_string):
    x = parse_expression(input_string)
    return x


def make_keyword_list(list):
    # ['x', 'y'] -> Keyword('x') | Keyword('y')
    return reduce(lambda x, y: x | y, map(Keyword, list))


def make_literal_list(list):
    # ['x', 'y'] -> Keyword('x') | Keyword('y')
    return reduce(lambda x, y: x | y, map(Literal, list))


def get_variable_value(toks):
    var, op = parsing.parse_unary_operator(toks)
    if type(var) is ml.Variable:
        if var.value in user_variables:
            return user_variables[var.value]
    return var


def get_decorator(toks):
    value, op = parsing.parse_unary_operator(toks)
    if type(value) is ml.Unit:
        value = value.convert_to_variable()
    value.add_decorator(op)
    return value


def get_equality_op(toks):
    t = toks[0]
    value1, value2, op = parsing.parse_binary_operator(toks, get_equality_op)
    hidden = False
    assignment = False
    if "equals" in t:
        type = "="
        if t["equals"]["modifier"]:
            if "#" in t["equals"]["modifier"]:
                value2 = evaluate_expression(value2)
            if "::" in t["equals"]["modifier"]:
                hidden = True
                if evaluate:
                    assign_variable(value1, value2)
            elif ":" in t["equals"]["modifier"]:
                if evaluate:
                    assign_variable(value1, value2)
    else:
        type = op[0]

    return ml.Equality(type, value1, value2, assignment, hidden)


def assign_variable(variable, value):
    global user_variables
    if type(variable) is ml.Equality:
        variable = variable.get_first()
    if type(variable) is ml.Unit:
        variable = variable.convert_to_variable()
    if type(variable) is ml.Variable:
        user_variables[variable.value] = value
    else:
        raise NameError(
            'Can only assign variables, not {}!'.format(type(variable)))


def evaluate_expression(expr, convert=True):
    if evaluate:
        return mProcess.evaluate(expr, __settings__["maple"], gui_mode, convert)
    return expr


def make_expression():

    ParserElement.setDefaultWhitespaceChars(' \t')

    deco_kw_list = make_keyword_list(decorator_keywords)
    equality_kw_list = make_keyword_list(equality_keywords)
    units_list = oneOf(units)
    unit_prefixes_list = oneOf(unit_prefixes)
    letters = alphas  # + alphas8bit
    chars = letters + nums
    space = White(' ')
    word_start = NotAny(chars)
    word_end = NotAny(chars)
    no_white = NotAny(White())

    expr = Forward()

    unit = (units_list + NotAny(no_white + Word(chars)) | (
        Optional(unit_prefixes_list + no_white) + units_list +
        NotAny(no_white + Word(chars)))) + NotAny(no_white + Literal('_'))

    name = NotAny(deco_kw_list | equality_kw_list | Keyword('cross')) + Word(
        letters, chars)

    variable = Forward()
    number = Forward()
    variable << Suppress(Optional(Literal('_') + no_white)) + name + \
        Optional(no_white + Literal('_') + no_white + (variable | number))

    function = Combine(name + Suppress("(")) + \
        delimitedList(expr, delim=',') + Suppress(")")

    number << (Combine(Word(nums) + Optional("." + Optional(Word(nums)))) +
               Optional(NotAny(White()) + (function | unit | variable)))

    eval_field = Suppress('#') + expr + Suppress('#')

    eval_direct_field = Suppress('$') + expr + Suppress('$')

    operand = (
        eval_field.setParseAction(lambda x: evaluate_expression(x[0]))
        | eval_direct_field.setParseAction(lambda x: evaluate_expression(x[0], False))
        | function.setParseAction(lambda x: parsing.get_function(x, functions))
        | unit.setParseAction(lambda x: parsing.get_unit(x, user_variables))
        | variable.setParseAction(
            lambda x: parsing.get_variable(x, variables, symbols))
        | number.setParseAction(parsing.get_value))

    insert_value = word_start + Literal('@') + no_white
    factop = no_white + Literal('!') + word_end
    signop = word_start + Literal('-') + no_white
    expop = Literal('^')
    fracop = Literal('/')
    multop1 = space.copy()
    multop2 = Literal('*')
    crossop = Keyword('cross')
    rangeop = Literal('..')
    plusop = oneOf('+ -')
    equals = Group(Regex(
        r'((?P<modifier>[:#])+(?P<option>[a-zA-Z]*))?=')).setResultsName(
            "equals")
    other_equals = oneOf('== <= >= < > ~~ ~ ~= ~== !=')
    equalop = Group(other_equals) | equals | Group(equality_kw_list)

    right = opAssoc.RIGHT
    left = opAssoc.LEFT
    expr << infixNotation(operand, [
        (insert_value, 1, right, get_variable_value),
        (factop, 1, left, parsing.get_factorial_op),
        (deco_kw_list, 1, right, get_decorator),
        (signop, 1, right, parsing.get_minus_op),
        (expop, 2, right, parsing.get_pow_op),
        (fracop, 2, left, parsing.get_div_op),
        (crossop, 2, left, parsing.get_cross_op),
        (multop1, 2, left, parsing.get_mul_op),
        (multop2, 2, left, parsing.get_mul_op),
        (plusop, 2, left, parsing.get_add_op),
        (rangeop, 2, left, parsing.get_range_op),
        (equalop, 2, left, get_equality_op)
    ])
    expr.parseWithTabs()
    return expr


expression = make_expression()


def parse(text, vars, eval=True, gui=False):
    global gui_mode
    global evaluate
    global user_variables
    gui_mode = gui
    evaluate = eval
    user_variables = vars
    if text == "":
        return ml.Empty()
    try:
        return expression.parseString(text)[0]
    except ParseException:
        return ml.Variable("ParseException")
