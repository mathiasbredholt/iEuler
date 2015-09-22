# latex generator for mathnotes
import mathlib


# generates LaTeX string from mathlib operators
def generate(input_expr):
    return convert_expr(input_expr)


def convert_expr(input_expr):
    return input_expr.to_latex()


def parentheses(input_expr):
    return "\\left( {} \\right)".format(input_expr.to_latex())


def convert_value(self):
    return self.value


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    if type(self.value1) is mathlib.Number and\
       type(self.value2) is mathlib.Number:
        output = "{} \\cdot {}"
    else:
        output = "{} {}"
    if type(self.value1) is mathlib.AddOp or\
       type(self.value1) is mathlib.SubOp:
        output_1 = parentheses(self.value1)
    else:
        output_1 = convert_expr(self.value1)
    if type(self.value2) is mathlib.AddOp or\
       type(self.value2) is mathlib.SubOp:
        output_2 = parentheses(self.value2)
    else:
        output_2 = convert_expr(self.value2)
    return output.format(output_1, output_2)


def convert_fraction(self):
    return "\\dfrac{{{}}}{{{}}} ".format(
        convert_expr(self.value1), convert_expr(self.value2))


def convert_power(self):
    if type(self.value1) is mathlib.Number or type(
            self.value1) is mathlib.Variable or type(
                    self.value1) is mathlib.Root:
        return "{}^{{{}}}".format(convert_expr(self.value1),
                                  convert_expr(self.value2))
    else:
        return "{}^{{{}}}".format(parentheses(self.value1),
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
mathlib.MathValue.to_latex = convert_value
mathlib.AddOp.to_latex = convert_addop
mathlib.SubOp.to_latex = convert_subop
mathlib.MulOp.to_latex = convert_mulop
mathlib.Fraction.to_latex = convert_fraction
mathlib.Power.to_latex = convert_power
mathlib.Root.to_latex = convert_power
mathlib.Integral.to_latex = convert_integral
mathlib.Derivative.to_latex = convert_derivative
