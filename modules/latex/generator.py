import mathlib as ml
import textlib as tl
from modules.latex.lib import *


def display_math(input_expr):
    if type(input_expr) is tl.Paragraph:
        return convert_expr(input_expr)
    return "$$ " + convert_expr(input_expr) + " $$"


def generate(input_expr, display=True, delimiters=True):
    result = convert_expr(input_expr, display)
    if not delimiters or type(input_expr) in [tl.Paragraph, tl.Text]:
        return result
    elif display:
        return "$$ " + result + " $$"
    else:
        return "$ " + result + " $"

    result = input_expr.to_latex()


def convert_expr(input_expr, display=True):
    if type(input_expr) is ml.Empty:
        return ""
    if type(input_expr) is ml.Fraction:
        return input_expr.to_latex(display)
    return input_expr.to_latex()


def parentheses(input_expr, do=True):
    if not type(input_expr) is str:
        input_expr = convert_expr(input_expr)
    if do:
        return "\\left( {} \\right)".format(input_expr)
    return input_expr


def convert_equality(self):
    if self.type in equalities:
        return "{} {} {}".format(convert_expr(self.value1),
                                 equalities[self.type],
                                 convert_expr(self.value2))
    else:
        return "{} {} {}".format(convert_expr(self.value1), self.type,
                                 convert_expr(self.value2))


def convert_paragraph(self):
    result = ""
    for x in self.blocks:
        result += convert_expr(x, display=False)
    return result


def convert_text(self):
    return self.text


def convert_value(self):
    if type(self) is ml.Unit:
        result = "\\mathrm{{{}}}".format(self.prefix + self.value)
    elif type(self) is ml.Ans:
        result = "ans{}".format(
            "_{" + convert_expr(self.index) + "}" if int(self.index.value) > 1 else "")
        return result
    elif type(self) is ml.Variable:
        if self.is_symbol:
            if self.value in special_symbols:
                result = special_symbols[self.value]
            else:
                result = "\\{}".format(self.value)
        else:
            result = self.value
        result = convert_decorators(self, result)
        if self.subscript:
            if len(self.subscript.name()) == 1:
                result += "_{}".format(convert_expr(self.subscript))
            else:
                result += "_{{{}}}".format(convert_expr(self.subscript))
        return result
    elif self.value[-1] == ".":
        result = self.value.strip(".")
    else:
        result = self.value
    return convert_decorators(self, result)


def convert_decorators(self, string):
    if self.get_decorators():
        for dec in self.get_decorators():
            if dec == "hat":
                string = "\\hat{{{}}}".format(string)
            elif dec == "bar":
                string = "\\bar{{{}}}".format(string)
            elif dec == "ul":
                string = "\\underline{{{}}}".format(string)
            elif dec == "vec":
                string = "\\boldsymbol{{\\mathbf{{{}}}}}".format(string)
            elif dec == "dot":
                string = "\\dot{{{}}}".format(string)
            elif dec == "ddot":
                string = "\\ddot{{{}}}".format(string)
            elif dec == "tdot":
                string = "\\dddot{{{}}}".format(string)
            elif dec == "arr" or dec == "arrow":
                string = "\\vec{{{}}}".format(string)

    return string


def convert_minus(self):
    return "-{}".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_factorial(self):
    return "{}!".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_function(self):
    name = "\\mathrm{{{}}}".format(self.name) if len(
        self.name) > 1 else self.name
    result = name + "\\left( " + convert_expr(self.value[0])
    for arg in self.value[1:]:
        result += ", " + convert_expr(arg)
    return result + " \\right)"


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    if self.is_dot():
        output = "{} \\cdot {}"
    else:
        output = "{} {}"
    num_after = type(self.value2) is ml.Number or type(self.value2) in [
        ml.MulOp, ml.Power
    ] and type(self.value2.get_first()) is ml.Number
    if num_after:
        output = "{} \\cdot {}"
    if type(self.value1) in [ml.AddOp, ml.SubOp]:
        output_1 = parentheses(self.value1)
    else:
        output_1 = convert_expr(self.value1)
    if type(self.value2) in [ml.AddOp, ml.SubOp]:
        output_2 = parentheses(self.value2)
    else:
        output_2 = convert_expr(self.value2)
    return output.format(output_1, output_2)


def convert_crossop(self):
    output = "{} \\times {}"
    output_1 = convert_expr(self.value1)
    output_2 = convert_expr(self.value2)
    return output.format(output_1, output_2)


def convert_fraction(self, display=True):
    # removed dfrac for compatibility issues with MathJax
    return "\\{}frac{{{}}}{{{}}} ".format("" if display else "",
                                          convert_expr(self.value1),
                                          convert_expr(self.value2))


def convert_power(self):
    if type(self.value1) in [ml.Number, ml.Variable, ml.Function, ml.Root,
                             ml.Unit]:
        return "{}^{{{}}}".format(convert_expr(self.value1),
                                  convert_expr(self.value2,
                                               display=False))
    else:
        return "{}^{{{}}}".format(parentheses(self.value1),
                                  convert_expr(self.value2,
                                               display=False))


def convert_root(self):
    if self.value2.get_value() == "2":
        return "\\sqrt{{{}}} ".format(convert_expr(self.value1))
    else:
        return "\\sqrt[{}]{{{}}} ".format(
            convert_expr(self.value2), convert_expr(self.value1))


def convert_integral(self):
    if self.variable is None:
        return "\\displaystyle \\int {}\\;d {} ".format(
            convert_expr(self.value), convert_expr(self.variable))
    else:
        return "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;d {} ".format(
            convert_expr(self.variable), convert_expr(self.variable),
            convert_expr(self.value), convert_expr(self.variable))


def convert_derivative(self):
    if self.nth.get_value() == "1":
        return "\\frac{{d}}{{d {}}}{} ".format(
            convert_expr(self.variable), convert_expr(self.value))
    else:
        return "\\frac{{d^{{{}}}}}{{d {}^{{{}}}}}{} ".format(
            convert_expr(self.nth), convert_expr(self.variable),
            convert_expr(self.nth), convert_expr(self.value))


def convert_range(self):
    return "\left[ \, {} \, ; {} \, \\right]".format(convert_expr(self.value1),
                                                     convert_expr(self.value2))

# Extending mathlib classes with to_latex method for duck typing
tl.Paragraph.to_latex = convert_paragraph
tl.Text.to_latex = convert_text
ml.MathValue.to_latex = convert_value
ml.Equality.to_latex = convert_equality
ml.Function.to_latex = convert_function
ml.Minus.to_latex = convert_minus
ml.Factorial.to_latex = convert_factorial
ml.AddOp.to_latex = convert_addop
ml.SubOp.to_latex = convert_subop
ml.MulOp.to_latex = convert_mulop
ml.CrossOp.to_latex = convert_crossop
ml.Fraction.to_latex = convert_fraction
ml.Power.to_latex = convert_power
ml.Root.to_latex = convert_root
ml.Integral.to_latex = convert_integral
ml.Derivative.to_latex = convert_derivative
ml.Range.to_latex = convert_range
