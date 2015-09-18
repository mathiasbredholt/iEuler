# maple parser for mathnotes
from mathlib import *
import re


def parse(input_string):
    # check for parentheses
    # re.findall("[()]", input_string)
    #
    # regexp = re.compile("\^\(1/[0-9]+\)")
    # result = regexp.search(input_string)
    return [[3, 5], Root(4, 2), Power(3, 6), Complex(3, 4)]
