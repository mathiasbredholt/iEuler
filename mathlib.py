# mathlib
# contains all datatypes


class Scalar:
    def __init__(self, value):
        self.value = value


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
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2


class Root:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value


class Power:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value
