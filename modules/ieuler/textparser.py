
import mathlib as ml
import textlib as tl
import parsing as parsing
from modules.ieuler.lib import *
from functools import reduce
import re
from pyparsing import *
import modules.maple.process as mProcess
import modules.tools.plot2d as plot2d

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def get_text(toks):
    return tl.Paragraph([tl.Text(toks[0])])


def make_expression():
    text = Word(printables + " ").leaveWhitespace().setParseAction(get_text)
    return text


expression = make_expression()


def parse(text):
    return expression.parseString(text)[0]
