# latex generator for mathnotes
import mathlib


# generates LaTeX string from mathlib operators
def generate(input_expr):
    settings = {"parentheses": False}
    return convert_expr(input_expr, settings)


def convert_expr(input_expr, settings):
    return input_expr.to_latex(settings)


def convert_value(self, settings):
    return self.value


def convert_addop(self, settings):
    if settings["parentheses"]:
        return "\\left({} + {}\\right)".format(
            convert_expr(self.value1, settings),
            convert_expr(self.value2, settings))
    else:
        return "{} + {}".format(convert_expr(self.value1, settings),
                                convert_expr(self.value2, settings))


def convert_subop(self, settings):
    if settings["parentheses"]:
        return "\\left({} - {}\\right)".format(
            convert_expr(self.value1, settings),
            convert_expr(self.value2, settings))
    else:
        return "{} - {}".format(convert_expr(self.value1, settings),
                                convert_expr(self.value2, settings))


def convert_mulop(self, settings):
    settings["parentheses"] = True
    if type(self.value1) is mathlib.Number and type(
            self.value2) is mathlib.Number:
        output = "{} \\cdot {}".format(convert_expr(self.value1, settings),
                                       convert_expr(self.value2, settings))
    else:
        output = "{} {}".format(convert_expr(self.value1, settings),
                                convert_expr(self.value2, settings))
    settings["parentheses"] = False
    return output


def convert_fraction(self, settings):
    return "\\dfrac{{{}}}{{{}}} ".format(
        convert_expr(self.value1, settings),
        convert_expr(self.value2, settings))


def convert_power(self, settings):
    return "{}^{{{}}}".format(convert_expr(self.value1, settings),
                              convert_expr(self.value2, settings))


def convert_root(self, settings):
    if self.value2.get_value is "2":
        return "\\sqrt{{{}}} ".format(convert_expr(self.value1, settings))
    else:
        return "\\sqrt[{}]{{{}}} ".format(
            convert_expr(self.value2, settings),
            convert_expr(self.value1, settings))


def convert_integral(self, settings):
    if self.range_from is None:
        return "\\displaystyle \\int {}\\;\partial {} ".format(
            convert_expr(self.value), convert_expr(self.dx))
    else:
        return "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;\partial {} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.dx))


def convert_derivative(self, settings):
    if self.nth.get_value is "1":
        return "\\frac{{\\partial {}}}{{\\partial {}}} ".format(
            convert_expr(self.dx), convert_expr(self.dy))
    else:
        return "\\frac{{\\partial^{{{}}}}}{{\\partial {}^{{{}}}}}{} ".format(
            convert_expr(self.nth), convert_expr(self.dy),
            convert_expr(self.nth), convert_expr(self.dx))

# Extending mathlib classes with to_latex method for duck typing
mathlib.MathValue.to_latex = convert_value
mathlib.AddOp.to_latex = convert_addop
mathlib.SubOp.to_latex = convert_subop
mathlib.MulOp.to_latex = convert_mulop
mathlib.Fraction.to_latex = convert_fraction
mathlib.Power.to_latex = convert_power
mathlib.Root.to_latex = convert_power
mathlib.Integral.to_latex = convert_integral
mathlib.Derivative.to_latex = convert_derivative
