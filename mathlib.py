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
        return self.value1.get_first()

    def __str__(self):
        return "Equality(type:'{}', {}, {})".format(self.type, self.value1,
                                                    self.value2)

    __repr__ = __str__


class MathValue:

    def get_value(self):
        return self.value

    def get_decorators(self):
        return self.decorators

    def get_first(self):
        return self

    def get_last(self):
        return self

    def get_variables(self):
        return []

    def is_matrix(self):
        return type(self) is Matrix or 'vec' in self.decorators

    def add_decorator(self, dec):
        decos = list(self.decorators)  # copy
        decos.append(dec)
        self.decorators = decos

    def add_attribute(self, attribute, value):
        attrs = self.attributes.copy()
        attrs[attribute] = value
        self.attributes = attrs

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

    def __init__(self, values):
        self.value = values
        self.decorators = []

    def get_variables(self):
        vars = []
        for r in self.value:
            for c in self.value[r]:
                vars += self.value[r][c].get_variables()
        return vars

    def height(self):
        return len(self.value)

    def width(self):
        return len(self.value[0])

    def __str__(self):
        return "Matrix({})".format(self.value)

    __repr__ = __str__


class Complex(MathValue):

    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
        self.value = (self.r, self.i)
        self.decorators = []

    def get_variables(self):
        return realpart.get_variables() + imagpart.get_variables()

    def __str__(self):
        return "Complex({})".format(self.value)

    __repr__ = __str__


class Variable(MathValue):

    def __init__(self, value, is_symbol=False, decs=[], subscript=None, attributes={}):
        self.value = value
        self.decorators = decs
        self.is_symbol = is_symbol
        self.subscript = subscript
        self.attributes = attributes

    def get_variables(self):
        return [self]

    def name(self):
        if self.subscript:
            return self.value + "_" + self.subscript.name()
        return self.value

    def __str__(self):
        return "Variable(name: {}, value: {} subscript: {} deco:{} symbol: {} attributes: {})".format(
            self.name(), self.value, self.subscript, self.decorators, "yes" if
            self.is_symbol else "no", self.attributes)

    __repr__ = __str__


class Ans(MathValue):

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def get_variables(self):
        return self.value.get_variables()

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

    def get_variables(self):
        vars = []
        for a in self.args:
            vars += a.get_variables()
        return vars

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

    def get_variables(self):
        return self.value.get_variables()

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

    def is_matrix(self):
        return self.value.is_matrix()

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

    def get_variables(self):
        return self.value1.get_variables() + self.value2.get_variables()

    def get_first(self):
        return self.value1.get_first()
        # if not self.value1.get_value():
        #     # value1 is an operator
        # else:
        #     # value1 is a value
        #     return self.value1

    def get_last(self):
        return self.value2.get_last()
        # if not self.value2.get_value():
        #     # value2 is an operator
        # else:
        #     # value2 is a value
        #     return self.value2

    def __str__(self):
        return "MathOperator({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class AddOp(MathOperator):

    def is_matrix(self):
        return self.value1.is_matrix() or self.value2.is_matrix()

    def __str__(self):
        return "AddOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class SubOp(MathOperator):

    def is_matrix(self):
        return self.value1.is_matrix() or self.value2.is_matrix()

    def __str__(self):
        return "SubOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class MulOp(MathOperator):

    def is_matrix(self):
        return self.value1.is_matrix() != self.value2.is_matrix()

    def is_dot(self):
        return self.value1.get_last().is_matrix() and self.value2.get_first().is_matrix()

    def __str__(self):
        return "MulOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class CrossOp(MathOperator):

    def is_matrix(self):
        return True

    def __str__(self):
        return "CrossOp({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Fraction(MathOperator):

    def is_matrix(self):
        return self.value1.is_matrix()

    def __str__(self):
        return "Fraction({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Root(MathOperator):

    def is_matrix(self):
        return False

    def __str__(self):
        return "Root({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Power(MathOperator):

    def is_matrix(self):
        return False

    def __str__(self):
        return "Power({},{})".format(self.value1, self.value2)

    __repr__ = __str__


class Range(MathOperator):

    def is_matrix(self):
        return value1.is_vector() and value2.is_vector()

    def __str__(self):
        return "Range({},{})".format(self.value1, self.value2)

    __repr__ = __str__

# Calculus


class Integral:

    def __init__(self, value, variable=None):
        self.value = value
        if type(variable) is Equality and type(variable.value2) is Range:
            self.variable = variable.value1
            self.range = variable.value2
            self.is_definite = True
        else:
            self.variable = variable
            self.range = None
            self.is_definite = False

    def get_first(self):
        return self

    def get_last(self):
        return self

    def is_matrix(self):
        return self.value.is_matrix()

    def get_value(self):
        return False

    def get_variables(self):
        return [] if self.variable is None else self.variable.get_variables()

    def __str__(self):
        return "Integral({},{})".format(self.value, self.variable)

    __repr__ = __str__


class Derivative:

    def is_matrix(self):
        return self.value.is_matrix()

    def __init__(self, value, variable, nth=Number("1")):
        self.value = value
        self.variable = variable
        self.nth = nth

    def get_first(self):
        return self

    def get_last(self):
        return self

    def get_value(self):
        return False

    def get_variables(self):
        return [] if self.variable is None else self.variable.get_variables()

    def __str__(self):
        return "Derivative({},{})".format(self.value, self.variable)

    __repr__ = __str__


class Sum:

    def is_matrix(self):
        return self.value.is_matrix()

    def __init__(self, value, variable=None):
        self.value = value
        if type(variable) is Equality and type(variable.value2) is Range:
            self.variable = variable.value1
            self.range = variable.value2
            self.has_limits = True
        else:
            self.variable = variable
            self.range = None
            self.has_limits = False

    def get_variables(self):
        return [x for x in self.value.get_variables() if x != self.variable]

    def get_value(self):
        return False

    def __str__(self):
        return "Sum({},{},{})".format(self.value, self.variable, self.range)

    __repr__ = __str__


class Limit:

    def is_matrix(self):
        return self.value.is_matrix()

    def get_variables(self):
        return [x for x in self.value.get_variables() if x != self.variable]

    def __init__(self, value, variable=None):
        self.value = value
        if type(variable) is Equality:  # or type is arrow operator
            self.variable = variable.value1
            self.limit = variable.value2
            self.has_limit = True
        else:
            self.variable = variable
            self.limit = None
            self.has_limit = False

    def get_value(self):
        return False

    def __str__(self):
        return "Limit({},{},{})".format(self.value, self.variable, self.limit)

    __repr__ = __str__
