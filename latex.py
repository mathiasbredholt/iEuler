# latex generator for mathnotes
from mathlib import *


def convert_expr(input_expr):
    if input_expr.get_value():
        return input_expr.get_value()
    else:
        output_string = ""
        if type(input_expr) is AddOp:
            return "{} + {}".format(convert_expr(input_expr.value1),
                                    convert_expr(input_expr.value2))
        elif type(input_expr) is SubOp:
            return "{} - {}".format(convert_expr(input_expr.value1),
                                    convert_expr(input_expr.value2))
        elif type(input_expr) is MulOp:
            if type(input_expr.value1) is Number and type(
                    input_expr.value2) is Number:
                return "{} \\cdot {}".format(convert_expr(input_expr.value1),
                                             convert_expr(input_expr.value2))
            else:
                return "{} {}".format(convert_expr(input_expr.value1),
                                      convert_expr(input_expr.value2))
        elif type(input_expr) is Fraction:
            return "\\dfrac{{{}}}{{{}}} ".format(
                convert_expr(input_expr.value1),
                convert_expr(input_expr.value2))
        elif type(input_expr) is Power:
            return "{}^{{{}}}".format(convert_expr(input_expr.value1),
                                      convert_expr(input_expr.value2))
        elif type(input_expr) is Root:
            if input_expr.value2.get_value is "2":
                return "\\sqrt{{{}}} ".format(convert_expr(input_expr.value1))
            else:
                return "\\sqrt[{}]{{{}}} ".format(
                    convert_expr(input_expr.value2),
                    convert_expr(input_expr.value1))
        elif type(input_expr) is Integral:
            return convert_integral(input_expr)

        elif type(input_expr) is Derivative:
            return convert_derivative(input_expr)


def convert_integral(input_expr):
    if input_expr.range_from is None:
        return "\\displaystyle \\int {}\\;\partial {} ".format(
            convert_expr(input_expr.value), convert_expr(input_expr.dx))
    else:
        return "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;\partial {} ".format(
            convert_expr(input_expr.range_from),
            convert_expr(input_expr.range_to), convert_expr(input_expr.value),
            convert_expr(input_expr.dx))


def convert_derivative(input_expr):
    if input_expr.nth.get_value is "1":
        return "\\frac{{\\partial {}}}{{\\partial {}}} ".format(
            convert_expr(input_expr.dx), convert_expr(input_expr.dy))
    else:
        return "\\frac{{\\partial^{{{}}}}}{{\\partial {}^{{{}}}}}{} ".format(
            convert_expr(input_expr.nth), convert_expr(input_expr.dy),
            convert_expr(input_expr.nth), convert_expr(input_expr.dx))
