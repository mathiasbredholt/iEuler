# maple parser for iEuler
import mathlib as ml
import parsing as parsing
from modules.maple.lib import *
import re
from pyparsing import *

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def parse(input_string):
    x = parse_expression(input_string)
    return x


def get_pow_op(toks):
    p = parsing.get_pow_op(toks)
    if (
            type(p.value2) is ml.Fraction and
            type(p.value2.value1) is ml.Number and p.value2.value1.value == "1" and
            not '.' in p.value2.value2.value):
        p = ml.Root(p.value1, p.value2.value2)
    return p


def make_expression():
    function = Forward()
    expression = Forward()
    number = Combine(Word(nums) + Optional("." + Word(nums))) | Combine(
        "." + Word(nums))
    variable = Word(alphas)
    operand = number.setParseAction(parsing.get_value) | function.setParseAction(
        lambda x: parsing.get_function(x, functions)) | variable.setParseAction(
            lambda x: parsing.get_variable(x, variables))
    function << Combine(Word(alphas) + Suppress("(")) + expression + \
        ZeroOrMore(Suppress(",") + expression) + Suppress(")")

    expop = Literal('^')
    signop = Literal('-')
    fracop = Literal('/')
    multop = Literal('*')
    plusop = oneOf('+ -')
    factop = Literal('!')

    expression << infixNotation(
        operand, [(factop, 1, opAssoc.LEFT, parsing.get_factorial_op),
                  (signop, 1, opAssoc.RIGHT, parsing.get_minus_op),
                  (expop, 2, opAssoc.RIGHT, get_pow_op),
                  (fracop, 2, opAssoc.LEFT, parsing.get_div_op),
                  (multop, 2, opAssoc.LEFT, parsing.get_mul_op),
                  (plusop, 2, opAssoc.LEFT, parsing.get_add_op)])
    return expression


expression = make_expression()


def parse(text):
    return expression.parseString(text)[0]
