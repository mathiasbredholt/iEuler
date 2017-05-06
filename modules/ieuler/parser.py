import json
from pyparsing import ParseException
from traceback import print_exc

from modules.ieuler.lib import *
import modules.ieuler.mathparser as math
import modules.ieuler.textparser as text


def parse(string, workspace, eval=True):
    if string == "":
        return ml.Empty()
    try:
        if string[0] == '%':
            return text.parse(string[1:])
        else:
            return math.parse(string, eval, workspace)
    except:
        print_exc()
        return ml.Variable("ParseException")
