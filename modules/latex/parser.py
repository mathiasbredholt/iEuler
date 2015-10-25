# latex generator for mathnotes
import mathlib as ml
import modules.tools.procio as procio
import json

__settings__ = None


def init():
    global __settings__

    with open('settings.conf', 'r') as f:
        __settings__ = json.load(f)["pdflatex"]


# generates LaTeX string from mathlib operators
def generate(input_expr):
    output_string = convert_expr(input_expr)
    with open("modules/latex/preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)
    with open("mathnotes.tex", "w") as f:
        f.write(output_string)

    proc, queue, thread = procio.run(
        __settings__ +
        " -interaction=batchmode -fmt pdflatex -shell-escape mathnotes.tex",
        False)
    proc.wait()
    proc, queue, thread = procio.run(
        "convert -density 300 mathnotes.pdf mathnotes.png", False)
    proc.wait()
    return output_string


def convert_expr(input_expr, display=True):
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
    return "{} {} {}".format(convert_expr(self.value1), self.type,
                             convert_expr(self.value2))


def convert_value(self):
    if type(self) is ml.Unit:
        result = "\\,\\mathrm{{{}}}".format(self.prefix + self.name)
    elif self.value == "pi":
        result = "\\pi"
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

    return string


def convert_minus(self):
    return "-{}".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_factorial(self):
    return "{}!".format(parentheses(self.value, not type(self.value) in
                                    [ml.Number, ml.Variable]))


def convert_function(self):
    result = self.name + "\\left( " + convert_expr(self.value[0])
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
    if self.range_from is None:
        return "\\displaystyle \\int {}\\;d {} ".format(
            convert_expr(self.value), convert_expr(self.variable))
    else:
        return "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;d {} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.variable))


def convert_derivative(self):
    if self.nth.get_value() == "1":
        return "\\frac{{d}}{{d {}}}{} ".format(
            convert_expr(self.variable), convert_expr(self.value))
    else:
        return "\\frac{{d^{{{}}}}}{{d {}^{{{}}}}}{} ".format(
            convert_expr(self.nth), convert_expr(self.variable),
            convert_expr(self.nth), convert_expr(self.value))

# Extending mathlib classes with to_latex method for duck typing
ml.MathValue.to_latex = convert_value
ml.Equality.to_latex = convert_equality
ml.Function.to_latex = convert_function
ml.Minus.to_latex = convert_minus
ml.Factorial.to_latex = convert_factorial
ml.AddOp.to_latex = convert_addop
ml.SubOp.to_latex = convert_subop
ml.MulOp.to_latex = convert_mulop
ml.Fraction.to_latex = convert_fraction
ml.Power.to_latex = convert_power
ml.Root.to_latex = convert_root
ml.Integral.to_latex = convert_integral
ml.Derivative.to_latex = convert_derivative
