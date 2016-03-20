# mathlib
# contains all datatypes


class Empty:

    def __init__(self):
        pass

    def __str__(self):
        return "Empty"

    __repr__ = __str__


class Equality:

    def __init__(self, type, value1, value2, assignment=False, hidden=False):
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.assignment = assignment
        self.hidden = hidden

    def get_first(self):
        if type(self.value1) is Equality:
            return self.value1.get_first()
        else:
            # value1 is a value
            return self.value1

    def __str__(self):
        return "Equality(type:'{}', {}, {})".format(self.type, self.value1,
                                                    self.value2)

    __repr__ = __str__


class MathValue:

    def get_value(self):
        return self.value

    def get_decorators(self):
        return self.decorators

    def is_vector(self):
        return type(self) is Matrix or 'vec' in self.decorators

    def add_decorator(self, dec):
        decos = list(self.decorators)  # copy
        decos.append(dec)
        self.decorators = decos

    def name(self):
        return self.value

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

    def __init__(self, value, is_symbol=False, decs=[], subscript=None):
        self.value = value
        self.decorators = decs
        self.is_symbol = is_symbol
        self.subscript = subscript

    def name(self):
        if self.subscript:
            return self.value + "_" + self.subscript.name()
        return self.value

    def __str__(self):
        return "Variable(name: {}, value: {} subscript: {} deco:{} symbol: {})".format(
            self.name(), self.value, self.subscript, self.decorators, "yes" if
            self.is_symbol else "no")

    __repr__ = __str__


class Ans(MathValue):

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __str__(self):
        return "Ans(index: {}, value: {})".format(
            self.index, self.value)

    __repr__ = __str__


class Unit(MathValue):

    def __init__(self, unit, prefix=""):
        self.value = unit
        self.prefix = prefix
        self.decorators = []

    def convert_to_variable(self):
        return Variable(self.prefix + self.value, False, self.decorators)

    def __str__(self):
        return "Unit({}, prefix: {})".format(self.value, self.prefix)

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

    def is_vector(self):
        return self.value.is_vector()

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

    def is_vector(self):
        return self.value1.is_vector() or self.value2.is_vector()

    def __str__(self):
        return "AddOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class SubOp(MathOperator):

    def is_vector(self):
        return self.value1.is_vector() or self.value2.is_vector()

    def __str__(self):
        return "SubOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class MulOp(MathOperator):

    def is_vector(self):
        return self.value1.is_vector() != self.value2.is_vector()

    def is_dot(self):
        return self.value1.is_vector() and self.value2.is_vector()

    def __str__(self):
        return "MulOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class CrossOp(MathOperator):

    def is_vector(self):
        return True

    def __str__(self):
        return "CrossOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Fraction(MathOperator):

    def is_vector(self):
        return self.value1.is_vector()

    def __str__(self):
        return "Fraction({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Root(MathOperator):

    def is_vector(self):
        return False

    def __str__(self):
        return "Root({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Power(MathOperator):

    def is_vector(self):
        return False

    def __str__(self):
        return "Power({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Range(MathOperator):

    def is_vector(self):
        return False

    def __str__(self):
        return "Range({},{})".format(self.value1, self.value2)

    __repr__ = __str__

# Calculus


class Integral:

    def is_vector(self):
        return self.value.is_vector()

    def __init__(self, value, variable):
        self.value = value
        self.variable = variable

    def get_value(self):
        return False

    def __str__(self):
        return "Integral({},{})".format(self.value, self.variable)

    __repr__ = __str__


class Derivative:

    def is_vector(self):
        return self.value.is_vector()

    def __init__(self, value, variable, nth=Number("1")):
        self.value = value
        self.variable = variable
        self.nth = nth

    def get_value(self):
        return False

    def __str__(self):
        return "Derivative({},{})".format(self.value, self.variable)

    __repr__ = __str__


class Sum:

    def is_vector(self):
        return self.value.is_vector()

    def __init__(self, value, variable):
        self.value = value
        self.variable = variable

        def get_value(self):
            return False

    def __str__(self):
        return "Sum({},{},{})".format(self.value, self.variable)

    __repr__ = __str__
