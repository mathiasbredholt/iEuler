# mathlib
# contains all datatypes


class MathValue:

    def get_value(self):
        return self.value

    def __str__(self):
        return "MathValue({})".format(self.value)

    __repr__ = __str__


class Number(MathValue):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Number({})".format(self.value)

    __repr__ = __str__


class Matrix(MathValue):

    def __init__(self, values, width, height):
        self.value = values
        self.width = width
        self.height = height

    def __str__(self):
        return "Matrix({})".format(self.value)

    __repr__ = __str__


class Complex(MathValue):

    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
        self.value = (self.r, self.i)

    def __str__(self):
        return "Complex({})".format(self.value)

    __repr__ = __str__


class Variable(MathValue):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Variable({})".format(self.value)

    __repr__ = __str__


class Function(MathValue):

    def __init__(self, name, args):
        self.value = args
        self.name = name

    def __str__(self):
        return "Function({},{})".format(self.name, self.value)

    __repr__ = __str__


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

    def __str__(self):
        return "MathOperator({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class AddOp(MathOperator):

    def __str__(self):
        return "AddOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class SubOp(MathOperator):

    def __str__(self):
        return "SubOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class MulOp(MathOperator):

    def __str__(self):
        return "MulOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Fraction(MathOperator):

    def __str__(self):
        return "Fraction({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Root(MathOperator):

    def __str__(self):
        return "Root({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Power(MathOperator):

    def __str__(self):
        return "Power({},{})".format(self.value1, self.value2)

    __repr__ = __str__

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
