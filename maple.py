# maple parser for mathnotes
from mathlib import *


def parse(input_string):
    return [[3, 3], MulOp, Complex(3, 4), AddOp, Root(2, 23)]
