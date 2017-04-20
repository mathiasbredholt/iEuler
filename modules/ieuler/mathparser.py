import iEuler.mathlib as ml
import iEuler.parsing as parsing
from iEuler.modules.ieuler.lib import *
import re
import copy
from iEuler.modules.pyparsing.pyparsing import *
from importlib import import_module

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def get_variable_value_op(toks, all=False):
    var, op = parsing.parse_unary_operator(toks)
    if all:
        return insert_all_variable_values(var)
    else:
        return insert_single_variable_value(var)


def insert_all_variable_values(var):
    vars1 = []
    vars2 = var.find(lambda x: type(x) in [ml.Variable, ml.Ans])
    while vars2 != vars1:
        var = insert_single_variable_value(var)
        vars1 = vars2
        vars2 = var.find(lambda x: type(x) in [ml.Variable, ml.Ans])
    return var


def insert_single_variable_value(var):
    #    print("var: {}".format(var))
    vars = var.find(lambda x: type(x) is ml.Ans or type(
        x) is ml.Variable and x.name() in user_variables)
    print("insert_single_variable_value>> vars: {}".format(vars))
    if len(vars) == 0:
        print("insert_single_variable_value>> len(vars)==0")
        return var
    if len(vars) > 1:
        print("insert_single_variable_value>> len(vars)>1")
        vars = [x for x in vars if len(x) == min(map(len, vars))]
        print("insert_single_variable_value>> vars: {}".format(vars))
    print("insert_single_variable_value>> loop")
    for v in vars:
        print("insert_single_variable_value>> var: {}, v: {}".format(var, v))
        print("insert_single_variable_value>> var.index(v): {}".format(var.index(v)))
        print("insert_single_variable_value>> get_variable_value(var.index(v)): {}".format(
            get_variable_value(var.index(v))))
        var = copy.deepcopy(var).replace(
            v, get_variable_value(var.index(v)))
    return var


def get_variable_value(obj):
    if type(obj) is ml.Variable:
        if obj.name() in user_variables:
            return user_variables[obj.name()]
    if type(obj) is ml.Ans and not type(obj.value) is ml.Empty:
        return obj.value
    return obj


def get_decorator(toks):
    value, op = parsing.parse_unary_operator(toks)
    if type(value) is ml.Unit:
        value = value.convert_to_variable()
    value.add_decorator(op)
    return value


def get_equality_op(toks):
    t = toks[0]
    value1, value2, op = parsing.parse_binary_operator(
        toks, get_equality_op)
    hidden = False
    assignment = False
    if "equals" in t:
        type = "="
        if t["equals"]["modifier"]:
            if "#" in t["equals"]["modifier"]:
                value2 = evaluate_expression(value2, t["equals"]["option"])
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


def get_attr_op(toks):
    t = toks[0]
    variable = t[0]
    if evaluate:
        if variable not in user_variables:
            user_variables[variable.name()] = variable

        if len(t) > 3:
            attribute = t[2]
            value = t[4]
            user_variables[variable.name()].add_attribute(attribute, value)
        else:
            decorator = t[2]
            user_variables[variable.name()].add_decorator(decorator)
    return variable


def assign_variable(variable, value):
    global user_variables
    if type(variable) is ml.Equality:
        variable = variable.get_first_value()
    if type(variable) is ml.Unit:
        variable = variable.convert_to_variable()
    if type(variable) is ml.Variable:
        user_variables[variable.name()] = value
    else:
        raise NameError(
            'Can only assign variables, not {}!'.format(type(variable)))


def evaluate_expression(expr, calculator="", convert=True):
    if evaluate:
        if not calculator:
            calculator = workspace["default_calculator"]
        if expr.find(lambda x: type(x) is ml.AnsPlaceholder):
            return expr
        return import_module("modules.{}.process".format(calculator)).evaluate(insert_all_variable_values(expr), convert)
    if convert:
        return insert_all_variable_values(expr)
    return ml.RawString(expr)


ParserElement.setDefaultWhitespaceChars(' ')

deco_kw_list = parsing.make_keyword_list(decorator_keywords)
equality_kw_list = parsing.make_keyword_list(equality_keywords)
units_list = oneOf(units['units'] + list(units['aliases'].keys()))
unit_prefixes_list = oneOf(
    units['prefixes'] + list(units['prefix_aliases'].keys()))


expression = Forward()

unit = Optional(Word(nums).setParseAction(parsing.get_value)) + Suppress(Literal(units['escape_character']) + parsing.no_white) + (
    units_list + NotAny(parsing.no_white + Word(parsing.chars)) | (
        Optional(unit_prefixes_list + parsing.no_white) + units_list +
        NotAny(parsing.no_white + Word(parsing.chars)))
) + NotAny(parsing.no_white + Literal(units['escape_character']))

other_unit = Suppress(Literal(units['escape_character']) + parsing.no_white) + Word(
    parsing.letters) + NotAny(parsing.no_white + Literal(units['escape_character']))

name = NotAny(deco_kw_list | equality_kw_list | Keyword('cross')) + Word(
    parsing.letters, parsing.chars)

variable = Forward()
number = Forward()

ans = Literal('ans') + Optional(~White() + Word(nums))

variable << name + Optional(parsing.no_white + Literal('_') + parsing.no_white
                            + (variable | number))

function = Combine(name + Suppress("(")) + \
    delimitedList(expression, delim=',') + Suppress(")")

matrix = Suppress(oneOf(matrix_delimiters["start"]) + Optional(White())) + expression + ZeroOrMore(oneOf(matrix_delimiters[
    "horizontal"] + matrix_delimiters["vertical"]) + NotAny(oneOf(matrix_delimiters["end"])) + expression) + Suppress(Optional(White()) + oneOf(matrix_delimiters["end"]))

number << (Combine(Word(nums) + Optional("." + NotAny(Literal('.')) + Optional(Word(nums)))) +
           Optional(NotAny(White()) + (function | unit | variable)))

eval_field = Suppress('#') + expression + Suppress('#') + \
    parsing.no_white + Optional(name)

escape_field = QuotedString("'") | QuotedString('"')

eval_direct_field = QuotedString("$")

abs_field = Suppress('|') + expression + Suppress('|')

operand = (
    eval_field.setParseAction(lambda x: evaluate_expression(
        x[0], "" if len(x) < 2 else x[1]))
    | escape_field.setParseAction(lambda x: parsing.get_variable(x, variables))
    | eval_direct_field.setParseAction(
        lambda x: evaluate_expression(x[0], convert=False))
    | abs_field.setParseAction(parsing.get_abs_op)
    | function.setParseAction(lambda x: parsing.get_function(x, functions))
    | unit.setParseAction(lambda x: parsing.get_unit(x, units))
    | other_unit.setParseAction(lambda x: parsing.get_unit(x, units, unknown=True))
    | ans.setParseAction(lambda x: parsing.get_ans(x, workspace))
    | variable.setParseAction(
        lambda x: parsing.get_variable(x, variables, symbols, user_variables))
    | matrix.setParseAction(lambda x: parsing.get_matrix(x, matrix_delimiters))
    | number.setParseAction(parsing.get_value)
)

insert_all_value = parsing.word_start + Literal('_@') + parsing.no_white
insert_value = parsing.word_start + Literal('@') + parsing.no_white
attrop = Literal('++') + Word(parsing.chars) + Optional(Literal(':') +
                                                        (escape_field | Word(parsing.chars)))
factop = parsing.no_white + Literal('!') + parsing.word_end
signop = parsing.word_start + Literal('-') + parsing.no_white
expop = Literal('^')
fracop = Literal('/')
multop1 = parsing.space.copy()
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
expression << infixNotation(operand, [
    (insert_all_value, 1, right, lambda x: get_variable_value_op(x, all=True)),
    (insert_value, 1, right, lambda x: get_variable_value_op(x, all=False)),
    (attrop, 1, left, get_attr_op),
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
expression.parseWithTabs()


def parse(text, eval, worksp):
    global workspace
    global user_variables
    global evaluate
    evaluate = eval
    workspace = worksp
    user_variables = worksp["user_variables"]
    return expression.parseString(text)[0]
