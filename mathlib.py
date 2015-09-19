# mathlib
# contains all datatypes


class Number:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class Matrix:
    def __init__(self, values, width, height):
        self.value = values
        self.width = width
        self.height = height


class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


class AddOp:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2


class SubOp:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2


class MulOp:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2


class Fraction:
    def __init__(self, enum, denom):
        self.enum = enum
        self.denom = denom


class Root:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value


class Power:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value


# Calculus
class Integral:
    def __init__(self, value, dx, range_from=None, range_to=None):
        self.value = value
        self.dx = dx
        self.range_from = range_from
        self.range_to = range_to


class Derivative:
    def __init__(self, dx, dy, nth):
        self.dx = dx
        self.dy = dy
        self.nth = nth
