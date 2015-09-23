# Command line interface for mathnotes
import mathlib


# generates string from mathlib operators
def generate(input_expr):
    return convert_expr(input_expr).replace("  ", " ")


def convert_expr(input_expr):
    return input_expr.to_cmd()


def parentheses(input_expr):
    return "( {} )".format(input_expr.to_cmd())


def convert_value(self):
    return self.value


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    output = "{} {}"
    if type(self.value1) is mathlib.Number and (
       type(self.value2) is mathlib.Number or
       type(self.value2) is mathlib.MulOp and type(self.value2.get_first()) is mathlib.Number) or\
            type(self.value2) is mathlib.Number:
        output = "{} * {}"
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
    return "({})/({}) ".format(
        convert_expr(self.value1), convert_expr(self.value2))


def convert_power(self):
    if type(self.value1) is mathlib.Number or\
       type(self.value1) is mathlib.Variable or\
       type(self.value1) is mathlib.Root:
        return "{}^({}) ".format(convert_expr(self.value1),
                                 convert_expr(self.value2))
    else:
        return "{}^({}) ".format(parentheses(self.value1),
                                 convert_expr(self.value2))


def convert_root(self):
    if self.value2.get_value is "2":
        return "sqrt({}) ".format(convert_expr(self.value1))
    else:
        return "root({}, {}) ".format(
            convert_expr(self.value1), convert_expr(self.value2))


def convert_integral(self):
    if self.range_from is None:
        return "int {} d{} ".format(
            convert_expr(self.value), convert_expr(self.dx))
    else:
        return "int from {} to {} d{} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.dx))


def convert_derivative(self):
    if self.nth.get_value is "1":
        return "d{}/d{} ".format(convert_expr(self.dx), convert_expr(self.dy))
    else:
        return "D({})({})({})".format(
            convert_expr(self.nth), convert_expr(self.dx),
            convert_expr(self.dy))

# Extending mathlib classes with to_cmd method for duck typing
mathlib.MathValue.to_cmd = convert_value
mathlib.AddOp.to_cmd = convert_addop
mathlib.SubOp.to_cmd = convert_subop
mathlib.MulOp.to_cmd = convert_mulop
mathlib.Fraction.to_cmd = convert_fraction
mathlib.Power.to_cmd = convert_power
mathlib.Root.to_cmd = convert_power
mathlib.Integral.to_cmd = convert_integral
mathlib.Derivative.to_cmd = convert_derivative


def print_math(math_list):
    output_string = ""
    for item in math_list:
        if type(item) is list:
            output_string += str(item) + " "
        elif type(item) is mathlib.Complex:
            output_string += "{} + {}i ".format(item.r, item.i)
        elif type(item) is mathlib.Root:
            output_string += "sqrt({}, {}) ".format(item.value, item.nth)
        elif type(item) is mathlib.Power:
            output_string += "{}^({}) ".format(item.value, item.nth)
    print(output_string)
