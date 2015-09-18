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
    def _init__(self, nth, val):
        self.n = nth
        self.value = val


class Power:
    def __init__(self, nth, val):
        self.n = nth
        self.value = val


def dummy():
    pass
