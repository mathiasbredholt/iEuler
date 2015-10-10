# maple parser for mathnotes
import procio
import mathlib as ml
import re
from pyparsing import ParserElement, Word, Literal, ZeroOrMore, Optional, Forward, Suppress, Combine, oneOf, infixNotation, opAssoc, nums, alphas

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


#################
# MAPLE PROCESS #
#################

def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


################################################
# GENERATE MAPLE STRING FROM MATHLIB OPERATORS #
################################################

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
ml.MathValue.to_maple = convert_value
ml.Minus.to_maple = convert_minus
ml.Factorial.to_maple = convert_factorial
ml.AddOp.to_maple = convert_addop
ml.SubOp.to_maple = convert_subop
ml.MulOp.to_maple = convert_mulop
ml.Fraction.to_maple = convert_fraction
ml.Power.to_maple = convert_power
ml.Root.to_maple = convert_root
ml.Integral.to_maple = convert_integral
ml.Derivative.to_maple = convert_derivative
ml.Function.to_maple = convert_function


###########################################
# PARSE MAPLE STRING TO MATHLIB OPERATORS #
###########################################

def parse(input_string):
    x = parse_expression(input_string)
    return x


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
                                  get_factorial_op),
                                 (signop, 1, opAssoc.RIGHT,
                                  get_minus_op),
                                 (expop, 2, opAssoc.RIGHT,
                                  get_pow_op),
                                 (fracop, 2, opAssoc.LEFT,
                                  get_div_op),
                                 (multop, 2, opAssoc.LEFT,
                                  get_mul_op),
                                 (plusop, 2, opAssoc.LEFT, get_add_op)]
                                )
    return expression


def get_function(toks):
    # print("toks={}".format(toks))
    name = toks[0]
    args = toks[1:]
    if name == "sqrt":
        return ml.Root(args[0], Number("2"))
    elif name == "int":
        return ml.Integral(args[0], args[1])
    elif name == "diff":
        return ml.Derivative(args[0], args[1])
    else:
        return ml.Function(name, args)


def get_value(toks):
    value = toks[0]
    # print("Value: {}".format(value))
    return ml.Number(value)


def get_variable(toks):
    name = toks[0]
    # print("Variable: {}".format(name))
    if name == "pi":
        return ml.Number(name)
    return ml.Variable(name)


def get_pow_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_pow_op)
    return ml.Power(value1, value2)


def get_mul_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_mul_op)
    return ml.MulOp(value1, value2)


def get_div_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_div_op)
    return ml.Fraction(value1, value2)


def get_add_op(toks):
    value1, value2, op = parse_binary_operator(toks, get_add_op)
    if op == "+":
        return ml.AddOp(value1, value2)
    else:
        return ml.SubOp(value1, value2)


def parse_binary_operator(toks, func):
    operator = toks[0][1]
    value1 = toks[0][0]
    if type(value1) is str:
        value1 = get_value(value1)
    if len(toks[0]) > 3:
        value2 = func([toks[0][2:]])
    else:
        value2 = toks[0][2]
        if type(value2) is str:
            value2 = get_value(value2)
    return value1, value2, operator


def get_factorial_op(toks):
    value, op = parse_unary_operator(toks, get_factorial_op, right=False)
    return ml.Factorial(value)


def get_minus_op(toks):
    value, op = parse_unary_operator(toks, get_minus_op)
    return ml.Minus(value)


def parse_unary_operator(toks, func, right=True):
    operator = toks[0][0 if right else -1]
    # print("Operator: {}".format(operator))
    value = toks[0][1 if right else 0]
    if type(value) is str:
        value = get_value(value)
    return value, operator


expression = make_expression()


def parse(text):
    return expression.parseString(text)[0]
