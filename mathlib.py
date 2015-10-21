# mathlib
# contains all datatypes


class Equality:

    def __init__(self, type, value1, value2, hidden=False):
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.hidden = hidden

    def __str__(self):
        return "Equality(type:'{}', {}, {})".format(self.type, self.value1, self.value2)

    __repr__ = __str__


class MathValue:

    def get_value(self):
        return self.value

    def get_decorators(self):
        return self.decorators

    def add_decorator(self, dec):
        self.decorators.append(dec)

    def __str__(self):
        return "MathValue({})".format(self.value)

    __repr__ = __str__


class Number(MathValue):

    def __init__(self, value):
        self.value = value
        self.decorators = []

    def __str__(self):
        return "Number({} {})".format(self.value, self.decorators)

    __repr__ = __str__


class Matrix(MathValue):

    def __init__(self, values, width, height):
        self.value = values
        self.width = width
        self.height = height
        self.decorators = []

    def __str__(self):
        return "Matrix({})".format(self.value)

    __repr__ = __str__


class Complex(MathValue):

    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
        self.value = (self.r, self.i)
        self.decorators = []

    def __str__(self):
        return "Complex({})".format(self.value)

    __repr__ = __str__


class Variable(MathValue):

    def __init__(self, value):
        self.value = value
        self.decorators = []

    def __str__(self):
        return "Variable({} {})".format(self.value, self.decorators)

    __repr__ = __str__


class Function(MathValue):

    def __init__(self, name, *args):
        self.value = args
        self.name = name
        self.decorators = []

    def __str__(self):
        return "Function({},{})".format(self.name, self.value)

    __repr__ = __str__


class Plot(MathValue):

    def __init__(self, value):
        self.value = value
        self.decorators = []

    def __str__(self):
        return "Plot({})".format(self.value)

    __repr__ = __str__


class MathUnaryOperator:

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return False

    def get_first(self):
        if not self.value.get_value():
            # value is an operator
            return self.value.get_first()
        else:
            # value is a value
            return self.value

    def get_last(self):
        return get_first(self)

    def __str__(self):
        return "MathUnaryOperator({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Minus(MathUnaryOperator):

    def __str__(self):
        return "Minus({})".format(self.value)

    __repr__ = __str__


class Factorial(MathUnaryOperator):

    def __str__(self):
        return "Factorial({})".format(self.value)

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
            # value2 is an operator
            return self.value2.get_last()
        else:
            # value2 is a value
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

    def __init__(self, value, variable, range_from=None, range_to=None):
        self.value = value
        self.variable = variable
        self.range_from = range_from
        self.range_to = range_to

    def get_value(self):
        return False

    def __str__(self):
        return "Integral({},{})".format(self.value, self.variable)

    __repr__ = __str__


class Derivative:

    def __init__(self, value, variable, nth=Number("1")):
        self.value = value
        self.variable = variable
        self.nth = nth

    def get_value(self):
        return False

    def __str__(self):
        return "Derivative({},{})".format(self.value, self.variable)

    __repr__ = __str__
