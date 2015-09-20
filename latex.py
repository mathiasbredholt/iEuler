# latex generator for mathnotes
import mathlib


# generates LaTeX string from list of mathlib operators
def generate(input_expr):
    output_string = ""
    for expr in input_expr:
        output_string += convert_expr(expr)
    return output_string


def convert_expr(input_expr):
    if input_expr.get_value():
        return input_expr.get_value()
    else:
        return input_expr.to_latex()


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    if type(self.value1) is mathlib.Number and type(
            self.value2) is mathlib.Number:
        return "{} \\cdot {}".format(convert_expr(self.value1),
                                     convert_expr(self.value2))
    else:
        return "{} {}".format(convert_expr(self.value1),
                              convert_expr(self.value2))


def convert_fraction(self):
    return "\\dfrac{{{}}}{{{}}} ".format(
        convert_expr(self.value1), convert_expr(self.value2))


def convert_power(self):
    return "{}^{{{}}}".format(convert_expr(self.value1),
                              convert_expr(self.value2))


def convert_root(self):
    if self.value2.get_value is "2":
        return "\\sqrt{{{}}} ".format(convert_expr(self.value1))
    else:
        return "\\sqrt[{}]{{{}}} ".format(
            convert_expr(self.value2), convert_expr(self.value1))


def convert_integral(self):
    if self.range_from is None:
        return "\\displaystyle \\int {}\\;\partial {} ".format(
            convert_expr(self.value), convert_expr(self.dx))
    else:
        return "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;\partial {} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.dx))


def convert_derivative(self):
    if self.nth.get_value is "1":
        return "\\frac{{\\partial {}}}{{\\partial {}}} ".format(
            convert_expr(self.dx), convert_expr(self.dy))
    else:
        return "\\frac{{\\partial^{{{}}}}}{{\\partial {}^{{{}}}}}{} ".format(
            convert_expr(self.nth), convert_expr(self.dy),
            convert_expr(self.nth), convert_expr(self.dx))

# Extending mathlib classes with to_latex method for duck typing
mathlib.AddOp.to_latex = convert_addop
mathlib.SubOp.to_latex = convert_subop
mathlib.MulOp.to_latex = convert_mulop
mathlib.Fraction.to_latex = convert_fraction
mathlib.Power.to_latex = convert_power
mathlib.Root.to_latex = convert_power
mathlib.Integral.to_latex = convert_integral
mathlib.Derivative.to_latex = convert_derivative
