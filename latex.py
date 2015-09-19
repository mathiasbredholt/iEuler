# latex generator for mathnotes
import mathlib


def generate(input_expr):
    output_string = ""
    for expr in input_expr:
        output_string += convert_expr(expr)
    return output_string


def convert_expr(input_expr):
    if input_expr.get_value():
        return input_expr.get_value()
    else:
        if type(input_expr) is mathlib.AddOp:
            return convert_addop(input_expr)

        elif type(input_expr) is mathlib.SubOp:
            return convert_subop(input_expr)

        elif type(input_expr) is mathlib.MulOp:
            return convert_mulop(input_expr)

        elif type(input_expr) is mathlib.Fraction:
            return convert_fraction(input_expr)

        elif type(input_expr) is mathlib.Root:
            return convert_root(input_expr)

        elif type(input_expr) is mathlib.Integral:
            return convert_integral(input_expr)

        elif type(input_expr) is mathlib.Derivative:
            return convert_derivative(input_expr)


def convert_addop(input_expr):
    return "{} + {}".format(convert_expr(input_expr.value1),
                            convert_expr(input_expr.value2))


def convert_subop(input_expr):
    return "{} - {}".format(convert_expr(input_expr.value1),
                            convert_expr(input_expr.value2))


def convert_mulop(input_expr):
    if type(input_expr.value1) is mathlib.Number and type(
            input_expr.value2) is mathlib.Number:
        return "{} \\cdot {}".format(convert_expr(input_expr.value1),
                                     convert_expr(input_expr.value2))
    else:
        return "{} {}".format(convert_expr(input_expr.value1),
                              convert_expr(input_expr.value2))


def convert_fraction(input_expr):
    return "\\dfrac{{{}}}{{{}}} ".format(
        convert_expr(input_expr.value1), convert_expr(input_expr.value2))


def convert_power(input_expr):
    return "{}^{{{}}}".format(convert_expr(input_expr.value1),
                              convert_expr(input_expr.value2))


def convert_root(input_expr):
    if input_expr.value2.get_value is "2":
        return "\\sqrt{{{}}} ".format(convert_expr(input_expr.value1))
    else:
        return "\\sqrt[{}]{{{}}} ".format(
            convert_expr(input_expr.value2), convert_expr(input_expr.value1))


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
