# Frink parser for iEuler
import mathlib as ml
import parsing as parsing
from modules.frink.lib import *
import re
from pyparsing import *
import parsing

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def make_expression():
    expression = Forward()

    word = Word(parsing.letters + "_", parsing.chars + "_")
    number = Combine(Word(nums) + Optional("." + Word(nums))) | Combine(
        "." + Word(nums))
    variable = word.copy()

    operand = (
        variable.setParseAction(lambda x: parsing.get_variable(x, variables))
        | number.setParseAction(parsing.get_value)
    )

    expop = Literal('^')
    signop = Literal('-')
    fracop = Literal('/')
    multop = Literal('*')
    plusop = oneOf('+ -')
    factop = Literal('!')
    equalop = Literal('=')

    expression << infixNotation(
        operand, [(factop, 1, opAssoc.LEFT, parsing.get_factorial_op),
                  (signop, 1, opAssoc.RIGHT, parsing.get_minus_op),
                  (expop, 2, opAssoc.RIGHT, parsing.get_pow_op),
                  (fracop, 2, opAssoc.LEFT, parsing.get_div_op),
                  (multop, 2, opAssoc.LEFT, parsing.get_mul_op),
                  (plusop, 2, opAssoc.LEFT, parsing.get_add_op),
                  (equalop, 2, opAssoc.LEFT, parsing.get_equal_op)])
    return expression


expression = make_expression()


def parse(input_string):
    print(input_string)
    return expression.parseString(input_string)[0]
