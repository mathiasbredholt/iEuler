# latex generator for mathnotes
from mathlib import *


def generate(math_expression):
    output_string = ""
    for item in math_expression:
        if type(item) is Number:
            output_string += item.value

        elif type(item) is Variable:
            output_string += item.name

        elif type(item) is AddOp:
            output_string += "+"

        elif type(item) is SubOp:
            output_string += "-"

        elif type(item) is MulOp:
            if type(item.value1) is Number and type(item.value2) is Number:
                output_string += "{} \\cdot {}".format(item.value1,
                                                       item.value2)
            else:
                output_string += "{} {}".format(item.value1, item.value2)

        elif type(item) is Fraction:
            output_string += "\\dfrac{{{}}}{{{}}} ".format(item.enum,
                                                           item.denom)

        elif type(item) is Root:
            if item.nth is 2:
                output_string += "\\sqrt{{{}}} ".format(item.value)
            else:
                output_string += "\\sqrt[{}]{{{}}} ".format(item.nth,
                                                            item.value)

        elif type(item) is Integral:
            if item.range_from is None:
                output_string += "\\displaystyle \\int {}\\;\partial {} ".format(
                    item.value, item.dx)
            else:
                output_string += "\\displaystyle \\int_{{{}}}^{{{}}} {}\\;\partial {} ".format(
                    item.range_from, item.range_to, item.value, item.dx)

        elif type(item) is Derivative:
            if item.nth is 1:
                output_string += "\\frac{{\\partial {}}}{{\\partial {}}} ".format(
                    item.dx, item.dy)
            else:
                output_string += "\\frac{{\\partial^{{{}}}}}{{\\partial {}^{{{}}}}}{} ".format(
                    item.nth, item.dy, item.nth, item.dx)

    return output_string
