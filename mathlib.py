# mathlib
# contains all datatypes


class Scalar:
    def __init__(self, value):
        self.value = value


class Vector:
    def __init__(self, values, width, height):
        self.value = values
        self.width = width
        self.height = height


class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


class AddOp:
    pass


class SubOp:
    pass


class MulOp:
    pass


class Fraction:
    pass


class Root:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value


class Power:
    def __init__(self, nth, value):
        self.nth = nth
        self.value = value


def dummy():
    pass
