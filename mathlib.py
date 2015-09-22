# mathlib
# contains all datatypes


class MathValue:

    def get_value(self):
        return self.value


class Number(MathValue):

    def __init__(self, value):
        self.value = value


class Matrix(MathValue):

    def __init__(self, values, width, height):
        self.value = values
        self.width = width
        self.height = height


class Complex(MathValue):

    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
        self.value = (self.r, self.i)


class Variable(MathValue):

    def __init__(self, value):
        self.value = value


class MathOperator:

    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def get_value(self):
        return False

    def get_first(self):
        if not self.value1.get_value():
            # value1 is an operator
            return self.value1.get_first()
        else:
            # value1 is a value
            return self.value1

    def get_last(self):
        if not self.value2.get_value():
            # value1 is an operator
            return self.value2.get_last()
        else:
            # value1 is a value
            return self.value2


class AddOp(MathOperator):
    pass


class SubOp(MathOperator):
    pass


class MulOp(MathOperator):
    pass


class Fraction(MathOperator):
    pass


class Root(MathOperator):
    pass


class Power(MathOperator):
    pass


# Calculus
class Integral:

    def __init__(self, value, dx, range_from=None, range_to=None):
        self.value = value
        self.dx = dx
        self.range_from = range_from
        self.range_to = range_to

    def get_value(self):
        return False


class Derivative:

    def __init__(self, dx, dy, nth):
        self.dx = dx
        self.dy = dy
        self.nth = nth

    def get_value(self):
        return False
