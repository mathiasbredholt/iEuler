# maple parser for mathnotes
import modules.tools.procio as procio
import mathlib as ml
import parsing as parsing
from modules.maple.lib import *
import re
from pyparsing import ParserElement, Word, Literal, ZeroOrMore, Optional, Forward, Suppress, Combine, oneOf, infixNotation, opAssoc, nums, alphas

ParserElement.enablePackrat()  # Vastly improves pyparsing performance

#################
# MAPLE PROCESS #
#################

maple_proc = None


def evaluate(expr, settings, gui_mode=False, convert=True):
    global maple_proc
    if maple_proc is None:
        # if not gui_mode:
        # print("Starting Maple...")
        # Spawn Maple subprocess.
        # Returns instance of process, queue and thread for
        # asynchronous I/O
        maple_proc = init(settings)
    return query(expr, *maple_proc, convert=convert)


def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def query(query, proc, queue, thread, convert=True):
    if convert:
        query = generate(query) + ";\n"
    proc.stdin.write(query)
    procio.process_input(proc, queue, thread, 0.5, True)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    return parse(return_string)

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
    if type(self) is ml.Unit:
        # TODO
        return ""
    return self.value


def convert_minus(self):
    return "-{}".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_factorial(self):
    return "{}!".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_equality(self):
    return "{} = {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
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
        return "int({}, {}) ".format(convert_expr(self.value),
                                     convert_expr(self.variable))
    else:
        return "int({}, {}={}..{}) ".format(
            convert_expr(self.value), convert_expr(self.variable),
            convert_expr(self.range_from), convert_expr(self.range_to))


def convert_derivative(self):
    if self.nth.get_value == "1":
        return "diff({}, {}) ".format(convert_expr(self.value),
                                      convert_expr(self.variable))
    else:
        return "diff({}, {}${}) ".format(convert_expr(self.value),
                                         convert_expr(self.variable),
                                         convert_expr(self.nth))


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
ml.Equality.to_maple = convert_equality
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
