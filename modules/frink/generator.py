# Frink generator for iEuler
import mathlib as ml
from modules.frink.lib import *


def generate(input_expr):
    return convert_expr(input_expr)


def convert_expr(input_expr):
    return input_expr.to_frink()


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
    output = "{} {}"
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

# Extending mathlib classes with to_frink method for duck typing
ml.MathValue.to_frink = convert_value
ml.Minus.to_frink = convert_minus
ml.Factorial.to_frink = convert_factorial
ml.Equality.to_frink = convert_equality
ml.AddOp.to_frink = convert_addop
ml.SubOp.to_frink = convert_subop
ml.MulOp.to_frink = convert_mulop
ml.Fraction.to_frink = convert_fraction
ml.Power.to_frink = convert_power
ml.Root.to_frink = convert_root
# ml.Function.to_frink = convert_function
