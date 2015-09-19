import mathlib


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
