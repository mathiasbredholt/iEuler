# maple parser for iEuler
import mathlib as ml
import parsing as parsing
from modules.maple.lib import *
import re
from pyparsing import *
import parsing

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def parse(input_string):
    x = parse_expression(input_string)
    return x


def get_pow_op(toks):
    p = parsing.get_pow_op(toks)
    if (
            type(p.value2) is ml.Fraction and
            type(p.value2.value1) is ml.Number and p.value2.value1.value == "1" and
            not '.' in p.value2.value2.value):
        p = ml.Root(p.value1, p.value2.value2)
    return p


def get_matrix(toks):
    if "Matrix" in toks[0]:
        type = "mat"
        rows = int(toks["rows"])
        cols = int(toks["columns"])
    elif "column" in toks[0]:
        type = "col_vec"
        rows = int(toks["rows"])
        cols = 1
    elif "row" in toks[0]:
        type = "row_vec"
        rows = 1
        cols = int(toks["columns"])

    matrix = [[0 for col in range(0, cols)] for row in range(0, rows)]
    shape = toks["shape"]
    if not shape:
        for item in toks["list"]:
            row = 1 if type == "row_vec" else int(item["row"])
            col = 1 if type == "col_vec" else int(item["col"])
            val = item["val"]
            matrix[row - 1][col - 1] = val
    else:
        pass

    return ml.Matrix(matrix)


def matrixParser(expression, word):
    return matrixVectorParser(expression, word, "mat")


def vectorColumnParser(expression, word):
    return matrixVectorParser(expression, word, "col_vec")


def vectorRowParser(expression, word):
    return matrixVectorParser(expression, word, "row_vec")


def matrixVectorParser(expression, word, type="all"):
    # Syntax:
    # Matrix(3,3,{},datatype = anything,storage = empty,order = Fortran_order,shape = [identity])
    # Matrix(2,3,{(1, 1) = 1, (1, 2) = 2, (1, 3) = 3, (2, 1) = 4, (2, 2) = 5,
    # (2, 3) = 6},datatype = anything,storage = rectangular,order =
    # Fortran_order,shape = [])
    delim = Suppress(Literal(","))
    rows = Word(nums).setResultsName("rows")
    columns = Word(nums).setResultsName("columns")
    if type == "mat":
        start = Literal('Matrix') + Suppress('(') + \
            rows + delim + columns + delim
    elif type == "row_vec":
        start = Literal('Vector[row]') + Suppress('(') + columns + delim
    elif type == "col_vec":
        start = Literal('Vector[column]') + Suppress('(') + rows + delim
    else:
        raise ValueError("Invalid argument " + type)

    end = Suppress(")")
    shape_start = Suppress(Literal("shape") + Literal("=") + Literal("["))
    shape_end = Suppress(Literal("]"))
    # shape = Literal("shape = []")
    shape = shape_start + Optional(word) + shape_end
    shape = shape.setResultsName("shape")
    element_list = matrixElementListParser(expression, type)
    argument = shape | element_list | expression
    argument_list = delimitedList(argument, delim=',')
    matrix = start + argument_list + end
    return matrix


def matrixElementListParser(expression, type):
    start = Suppress(Literal("{"))
    end = Suppress(Literal("}"))
    if type == "mat":
        coords_start = Suppress(Literal("("))
        coords_end = Suppress(Literal(")"))
        coords_delimiter = Suppress(Literal(","))
        coords_row = Word(nums).setResultsName("row")
        coords_col = Word(nums).setResultsName("col")
        coords = coords_start + coords_row + coords_delimiter + coords_col + coords_end
    elif type == "row_vec":
        coords = Word(nums).setResultsName("col")
    elif type == "col_vec":
        coords = Word(nums).setResultsName("row")
    else:
        raise ValueError("Invalid argument " + type)

    value = expression.setResultsName("val")
    element = Group(coords + Suppress(Literal("=")) + value)
    element_list = start + Optional(delimitedList(element, delim=',')) + end
    element_list = element_list.setResultsName("list")
    return element_list


def make_expression():
    expression = Forward()

    word = Word(parsing.letters + "_", parsing.chars + "_")
    matrix = matrixParser(expression, word) | vectorRowParser(
        expression, word) | vectorColumnParser(expression, word)
    number = Combine(Word(nums) + Optional("." + Word(nums))) | Combine(
        "." + Word(nums))
    variable = word.copy()
    function = Combine(word + Suppress("(")) + \
        delimitedList(expression, delim=',') + Suppress(")")

    operand = (
        matrix.setParseAction(get_matrix)
        | function.setParseAction(lambda x: parsing.get_function(x, functions))
        | variable.setParseAction(lambda x: parsing.get_variable(x, variables))
        | number.setParseAction(parsing.get_value)
    )

    expop = Literal('^')
    signop = Literal('-')
    fracop = Literal('/')
    multop = Literal('*')
    plusop = oneOf('+ -')
    factop = Literal('!')
    equalop = Literal('=')

    expression << infixNotation(
        operand, [(factop, 1, opAssoc.LEFT, parsing.get_factorial_op),
                  (signop, 1, opAssoc.RIGHT, parsing.get_minus_op),
                  (expop, 2, opAssoc.RIGHT, get_pow_op),
                  (fracop, 2, opAssoc.LEFT, parsing.get_div_op),
                  (multop, 2, opAssoc.LEFT, parsing.get_mul_op),
                  (plusop, 2, opAssoc.LEFT, parsing.get_add_op),
                  (equalop, 2, opAssoc.LEFT, parsing.get_equal_op)])
    return expression


expression = make_expression()


def parse(text):
    return expression.parseString(text)[0]
