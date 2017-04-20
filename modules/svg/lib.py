import iEuler.mathlib as ml
import textlib as tl


class MathOperator(ml.MathOperator):
    style = "normal"


class AddOp(ml.AddOp):
    text = "+"
    width = 15


class SubOp(ml.SubOp):
    text = "-"
    width = 15


class Integral(ml.Integral):
    text = "&#x222B;"
    style = "normal"
    width = 15
    height = 20
    size = 24


class Sum(ml.Sum):
    text = "&#x2211;"
    width = 15
    height = 20
    size = 24
