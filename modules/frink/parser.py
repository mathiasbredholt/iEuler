# Frink parser for iEuler
import mathlib as ml
import parsing as parsing
from modules.frink.lib import *
import re
from pyparsing import *
import parsing

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def get_value(toks):
    number = parsing.get_value(toks).value
    # print("number: {}".format(number))
    exponent = 0
    if number[0:3] == '0.0':
        # Convert to power of 10 notation for all numbers < 0.1
        while number[0:2] == '0.':
            number = number[2:5] + '.' + number[5:]
            number = number.strip('0')
            if number[0] == '.':
                number = '0' + number
            exponent -= 3
    i = number.find('.')
    if i > 3:
        # Convert to power of 10 notation for all numbers >= 1000
        exponent = (i - 1) // 3 * 3
        number = number[:i - exponent] + '.' + \
            number[i - exponent:].replace('.', '')
    # print("i: {}, exponent: {}, number: {}".format(i, exponent, number))
    if exponent != 0:
        # Convert to power of 10 notation
        e = ml.Number(str(exponent)) if exponent >= 0 else ml.Minus(
            ml.Number(str(-exponent)))
        power = ml.Power(ml.Number('10'), e)
        return ml.MulOp(ml.Number(number), power)
    return ml.Number(number)


def get_scientific(toks):
    # Convert scientific notation (2e3) to power of 10 notation (2*10^3)
    number = toks[0]
    exponent = int(toks[3])
    if type(number) is ml.MulOp:
        exponent += int(number.value2.value2.value)
        number = number.value1
    exponent = ml.Number(str(exponent))
    if toks[2] == '-':
        exponent = ml.Minus(exponent)
    power = ml.Power(ml.Number('10'), exponent)
    return ml.MulOp(number, power)


def get_mul_op(toks):
    res = parsing.get_mul_op(toks)

    if type(res.value2) is ml.Unit and type(res.value1) is ml.MulOp and type(res.value1.value2) is ml.Power and type(res.value1.value2.value1) is ml.Number and res.value1.value2.value1.value == '10':
        # Expression matches format val*10^x*unit
        # convert to decadic prefix on unit
        exponent = 0 if res.value2.prefix == '' else units[
            'prefixes'][res.value2.prefix]
        if type(res.value1.value2.value2) is ml.Number and res.value1.value2.value2.value.isdigit():
            # x is a positive integer
            exponent += int(res.value1.value2.value2.value)
        elif type(res.value1.value2.value2) is ml.Minus and res.value1.value2.value2.value.value.isdigit():
            # x is a negative integer
            exponent -= int(res.value1.value2.value2.value.value)
        if exponent in units['prefixes'].values():
            # Only perform the conversion if there is a corresponding decadic prefix
            # This is not a problem since all exponents should be multiples of
            # 3.
            inv_prefix = {v: k for k, v in units['prefixes'].items()}
            res.value1 = res.value1.value1
            res.value2.prefix = inv_prefix[exponent]
    return res


def make_expression():
    expression = Forward()

    units_list = oneOf(units['units'] + list(units['aliases'].keys()))
    unit_prefixes_list = oneOf(
        list(units['prefixes'].keys()) + list(units['prefix_aliases'].keys()))

    number = Combine(Word(nums) + Optional("." + Word(nums))) | Combine(
        "." + Word(nums))

    scientific_notation = number + parsing.no_white + \
        Literal('e') + parsing.no_white + oneOf('+ -') + \
        parsing.no_white + Word(nums)

    unit = units_list + NotAny(parsing.no_white + Word(parsing.chars)) | (Optional(
        unit_prefixes_list + parsing.no_white) + units_list + NotAny(parsing.no_white + Word(parsing.chars)))

    operand = (
        unit.setParseAction(lambda x: parsing.get_unit(x, units))
        | scientific_notation.setParseAction(get_scientific)
        | number.setParseAction(get_value)
    )

    expop = Literal('^')
    signop = Literal('-')
    fracop = Literal('/')
    multop = parsing.space.copy()
    plusop = oneOf('+ -')
    factop = Literal('!')
    equalop = Literal('=')

    expression << infixNotation(
        operand, [(factop, 1, opAssoc.LEFT, parsing.get_factorial_op),
                  (signop, 1, opAssoc.RIGHT, parsing.get_minus_op),
                  (expop, 2, opAssoc.RIGHT, parsing.get_pow_op),
                  (fracop, 2, opAssoc.LEFT, parsing.get_div_op),
                  (multop, 2, opAssoc.LEFT, get_mul_op),
                  (plusop, 2, opAssoc.LEFT, parsing.get_add_op),
                  (equalop, 2, opAssoc.LEFT, parsing.get_equal_op)])
    return expression


expression = make_expression()


def parse(input_string):
    print(input_string)
    return expression.parseString(input_string)[0]
