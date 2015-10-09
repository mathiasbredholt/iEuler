# Command line interface for mathnotes
import mathlib as ml
import math

__plot_vars__ = {}


def set_plot_variables(variables):
    global __plot_vars__
    __plot_vars__ = variables


# generates string from mathlib operators
def parse(input_expr):
    return convert_expr(input_expr)


def convert_expr(input_expr):
    return input_expr.to_numpy()


def parentheses(input_expr, do=True):
    if not type(input_expr) is str:
        input_expr = convert_expr(input_expr)
    if do:
        return "( {} )".format(input_expr)
    return input_expr


def convert_variable(self):
    global __plot_vars__
    try:
        return __plot_vars__[self.value]
    except KeyError as err:
        print('Variable not in expression.')


def convert_number(self):
    return int(self.value)


def convert_minus(self):
    return -self.value


def convert_factorial(self):
    return math.factorial(self.value)


def convert_addop(self):
    return convert_expr(self.value1) + convert_expr(self.value2)


def convert_subop(self):
    return convert_expr(self.value1) - convert_expr(self.value2)


def convert_mulop(self):
    return convert_expr(self.value1) * convert_expr(self.value2)


def convert_fraction(self):
    return convert_expr(self.value1) / convert_expr(self.value2)


def convert_power(self):
    return convert_expr(self.value1) ** convert_expr(self.value2)


def convert_root(self):
    return convert_expr(self.value1) ** (1 / convert_expr(self.value2))


def convert_integral(self):
    return None
    # if self.range_from is None:
    #     return "int {} d{} ".format(
    #         convert_expr(self.value), convert_expr(self.variable))
    # else:
    #     return "int from {} to {} d{} ".format(
    #         convert_expr(self.range_from), convert_expr(self.range_to),
    #         convert_expr(self.value), convert_expr(self.variable))


def convert_derivative(self):
    return None
    # if self.nth.get_value == "1":
    #     return "d{}/d{} ".format(convert_expr(self.value),
    #                              convert_expr(self.variable))
    # else:
    #     return "D({})({})({})".format(
    #         convert_expr(self.nth), convert_expr(self.value),
    #         convert_expr(self.variable))


def convert_function(self):
    return None
    # text = self.name
    # text += "("
    # for i, arg in enumerate(self.value):
    #     if i != 0:
    #         text += ", "
    #     text += convert_expr(arg)
    # text += ")"
    # return text

    # Extending mathlib classes with to_numpy method for duck typing


ml.Variable.to_numpy = convert_variable
ml.Number.to_numpy = convert_number
ml.Minus.to_numpy = convert_minus
ml.Factorial.to_numpy = convert_factorial
ml.AddOp.to_numpy = convert_addop
ml.SubOp.to_numpy = convert_subop
ml.MulOp.to_numpy = convert_mulop
ml.Fraction.to_numpy = convert_fraction
ml.Power.to_numpy = convert_power
ml.Root.to_numpy = convert_root
ml.Integral.to_numpy = convert_integral
ml.Derivative.to_numpy = convert_derivative
ml.Function.to_numpy = convert_function


def print_math(math_list):
    output_string = ""
    for item in math_list:
        if type(item) is list:
            output_string += str(item) + " "
        elif type(item) is ml.Complex:
            output_string += "{} + {}i ".format(item.r, item.i)
        elif type(item) is ml.Root:
            output_string += "sqrt({}, {}) ".format(item.value, item.nth)
        elif type(item) is ml.Power:
            output_string += "{}^({}) ".format(item.value, item.nth)
    print(output_string)
