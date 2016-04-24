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

    def flatten(self):
        val1 = self.value1.flatten() if type(
            self.value1) is Equality else [self.value1]
        val2 = self.value2.flatten() if type(
            self.value2) is Equality else [self.value2]
        return val1 + val2

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value1.find(x, i, index + [0])
        self.value2.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        return self.value1.index(rest) if index == 0 else self.value2.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value1 = val
            else:
                self.value2 = val
        elif index == 0:
            self.value1.replace(rest, val)
        else:
            self.value2.replace(rest, val)
        return self

    # def has(self, type):
    # return type(self) is type or self.value1.has(type) or
    # self.value2.has(type)

    def get_first_value(self):
        return self.value1.get_first_value()

    def get_last_value(self):
        return self.value2.get_last_value()

    def get_first_expression(self):
        return self.value1.get_first_expression()

    def get_last_expression(self):
        return self.value2.get_last_expression()

    def __str__(self):
        return "Equality(type:'{}', {}, {})".format(self.type, self.value1,
                                                    self.value2)

    __repr__ = __str__


class MathValue:

    def get_value(self):
        return self.value

    def get_decorators(self):
        return self.decorators

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
#        print("i: {}, index: {}, x: {}, type: {}, same: {}".format(
#            i, index, x, type(self), type(self) is x))
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if not len(i) == 0:
            raise IndexError()
        else:
            return self

    def replace(self, i, val):
        if not len(i) == 0:
            raise IndexError()
        else:
            return val

    def get_first_value(self):
        return self

    def get_last_value(self):
        return self

    def get_first_expression(self):
        return self

    def get_last_expression(self):
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


class RawString(MathValue):

    def __init__(self, value):
        self.value = value
        self.decorators = []

    def __str__(self):
        return "RawString(\"{}\")".format(self.value)

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

    def __init__(self, value, index=Number('1')):
        self.value = value
        self.index = index

    def get_variables(self):
        return self.value.get_variables()

    def __str__(self):
        return "Ans(index: {}, value: {})".format(
            self.index, self.value)

    __repr__ = __str__


class Unit(MathValue):

    def __init__(self, unit, prefix="", unknown=False):
        self.value = unit
        self.prefix = prefix
        self.decorators = []
        self.unknown = unknown

    def convert_to_variable(self):
        return Variable(self.prefix + self.value, False, self.decorators)

    def __str__(self):
        return "Unit({}, prefix: {}, unknown: {})".format(self.value, self.prefix, self.unknown)

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

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value.find(x, i, index + [0])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index == 0:
            raise IndexError()
        return self.value.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index == 0:
            raise IndexError()
        if len(rest) == 0:
            self.value = val
        else:
            self.value.replace(rest, val)
        return self

    def get_value(self):
        return False

    def get_first_value(self):
        return self.value.get_first_value()
        # if not self.value.get_value():
        #     # value is an operator
        #     return self.value.get_first_value()
        # else:
        #     # value is a value
        #     return self.value

    def get_last_value(self):
        return self.get_first_value()

    def is_matrix(self):
        return self.value.is_matrix()

    def get_first_expression(self):
        return self

    def get_last_expression(self):
        return self

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

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value1.find(x, i, index + [0])
        self.value2.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        return self.value1.index(rest) if index == 0 else self.value2.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value1 = val
            else:
                self.value2 = val
        elif index == 0:
            self.value1.replace(rest, val)
        else:
            self.value2.replace(rest, val)
        return self

    def get_value(self):
        return False

    def get_variables(self):
        return self.value1.get_variables() + self.value2.get_variables()

    def get_first_value(self):
        return self.value1.get_first_value()
        # if not self.value1.get_value():
        #     # value1 is an operator
        # else:
        #     # value1 is a value
        #     return self.value1

    def get_last_value(self):
        return self.value2.get_last_value()
        # if not self.value2.get_value():
        # else:
        #     # value2 is a value
        #     return self.value2

    def get_first_expression(self):
        return self

    def get_last_expression(self):
        return self

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
        return self.value1.get_last_value().is_matrix() and self.value2.get_first_value().is_matrix()

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

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value.find(x, i, index + [0])
        if variable:
            self.variable.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        return self.value.index(rest) if index == 0 else self.variable.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value = val
            else:
                self.variable = val
        elif index == 0:
            self.value.replace(rest, val)
        else:
            self.variable.replace(rest, val)
        return self

    def get_first_value(self):
        return self

    def get_last_value(self):
        return self

    def get_first_expression(self):
        return self

    def get_last_expression(self):
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

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value.find(x, i, index + [0])
        self.variable.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        return self.value.index(rest) if index == 0 else self.variable.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1]:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value = val
            else:
                self.variable = val
        elif index == 0:
            self.value.replace(rest, val)
        else:
            self.variable.replace(rest, val)
        return self

    def get_first_value(self):
        return self

    def get_last_value(self):
        return self

    def get_first_expression(self):
        return self

    def get_last_expression(self):
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

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value.find(x, i, index + [0])
        if variable:
            self.variable.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        return self.value.index(rest) if index == 0 else self.variable.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value = val
            else:
                self.variable = val
        elif index == 0:
            self.value.replace(rest, val)
        else:
            self.variable.replace(rest, val)
        return self

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

    def get_first_value(self):
        return self

    def get_last_value(self):
        return self

    def get_first_expression(self):
        return self

    def get_last_expression(self):
        return self

    def get_variables(self):
        return [x for x in self.value.get_variables() if x != self.variable]

    def get_value(self):
        return False

    def __str__(self):
        return "Sum({},{},{})".format(self.value, self.variable, self.range)

    __repr__ = __str__


class Limit:

    def find(self, x, i=None, index=[]):
        if i is None:
            i = []
        self.value.find(x, i, index + [0])
        if variable:
            self.variable.find(x, i, index + [1])
        if type(self) is x:
            i += [index]
        return i

    def index(self, i):
        if len(i) == 0:
            return self
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        return self.value.index(rest) if index == 0 else self.variable.index(rest)

    def replace(self, i, val):
        if len(i) == 0:
            return val
        index = i[0]
        rest = i[1:]
        if not index in [0, 1] or index == 1 and variable is None:
            raise IndexError()
        if len(rest) == 0:
            if index == 0:
                self.value = val
            else:
                self.variable = val
        elif index == 0:
            self.value.replace(rest, val)
        else:
            self.variable.replace(rest, val)
        return self

    def is_matrix(self):
        return self.value.is_matrix()

    def get_variables(self):
        return [x for x in self.value.get_variables() if x != self.variable]

    def get_first_value(self):
        return self

    def get_last_value(self):
        return self

    def get_first_expression(self):
        return self

    def get_last_expression(self):
        return self

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
