
import mathlib as ml
import textlib as tl
import parsing
from modules.ieuler.lib import *
import re
from pyparsing import *
import modules.ieuler.mathparser as math
import modules.tools.plot2d as plot2d

ParserElement.enablePackrat()  # Vastly improves pyparsing performance


def get_text(toks):
    print(toks)
    return tl.Paragraph([tl.Text(toks[0])])


quickmath = Suppress(Literal('_') + parsing.no_white) + \
    (math.number | math.variable | math.function)
text = Word(printables.replace('_', '') +
            " ").leaveWhitespace().setParseAction(get_text)
quickmath.setParseAction(print)


expression = ZeroOrMore(quickmath | text)


def parse(text):
    return expression.parseString(text)[0]
