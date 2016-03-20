from modules.ieuler.lib import *
import modules.ieuler.mathparser as math
import modules.ieuler.textparser as text
import json
from pyparsing import ParseException


def parse(string, workspace, eval=True):
    if string == "":
        return ml.Empty()
    try:
        if string[0] == '%':
            return text.parse(string[1:])
        else:
            return math.parse(string, workspace)
    except ParseException:
        return ml.Variable("ParseException")
