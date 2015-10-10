# Command line interface for mathnotes
import mathlib as ml


# generates string from mathlib operators
def generate(input_expr):
    return convert_expr(input_expr)


def convert_expr(input_expr):
    return input_expr.to_cmd()


def parentheses(input_expr, do=True):
    if not type(input_expr) is str:
        input_expr = convert_expr(input_expr)
    if do:
        return "( {} )".format(input_expr)
    return input_expr


def convert_equality(self):
    return "{} {} {}".format(convert_expr(self.value1), self.type, convert_expr(self.value2))


def convert_value(self):
    return self.value


def convert_minus(self):
    return "-{}".format(parentheses(self.value, not type(self.value) in [ml.Number, ml.Variable]))


def convert_factorial(self):
    return "{}!".format(parentheses(self.value, not type(self.value) in [ml.Number, ml.Variable]))


def convert_addop(self):
    return "{} + {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_subop(self):
    return "{} - {}".format(convert_expr(self.value1),
                            convert_expr(self.value2))


def convert_mulop(self):
    output = "{} {}"
    num_after = type(self.value2) is ml.Number or type(self.value2) in [
        ml.MulOp, ml.Power] and type(self.value2.get_first()) is ml.Number
    if num_after:
        output = "{} * {}"
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
        parentheses(self.value1, type(self.value1) in [ml.AddOp, ml.SubOp]), parentheses(self.value2, not type(self.value2) in [ml.Number, ml.Variable]))


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


def convert_integral(self):
    if self.range_from is None:
        return "int {} d{} ".format(
            convert_expr(self.value), convert_expr(self.variable))
    else:
        return "int from {} to {} d{} ".format(
            convert_expr(self.range_from), convert_expr(self.range_to),
            convert_expr(self.value), convert_expr(self.variable))


def convert_derivative(self):
    if self.nth.get_value == "1":
        return "d{}/d{} ".format(convert_expr(self.value), convert_expr(self.variable))
    else:
        return "D({})({})({})".format(
            convert_expr(self.nth), convert_expr(self.value),
            convert_expr(self.variable))


def convert_function(self):
    text = self.name
    text += "("
    for i, arg in enumerate(self.value):
        if i != 0:
            text += ", "
        text += convert_expr(arg)
    text += ")"
    return text

# Extending mathlib classes with to_cmd method for duck typing
ml.Equality.to_cmd = convert_equality
ml.MathValue.to_cmd = convert_value
ml.Minus.to_cmd = convert_minus
ml.Factorial.to_cmd = convert_factorial
ml.AddOp.to_cmd = convert_addop
ml.SubOp.to_cmd = convert_subop
ml.MulOp.to_cmd = convert_mulop
ml.Fraction.to_cmd = convert_fraction
ml.Power.to_cmd = convert_power
ml.Root.to_cmd = convert_root
ml.Integral.to_cmd = convert_integral
ml.Derivative.to_cmd = convert_derivative
ml.Function.to_cmd = convert_function


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
