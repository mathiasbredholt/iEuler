
from modules.ieuler.lib import *
import modules.ieuler.mathparser as math
import modules.ieuler.textparser as text
import json
from pyparsing import ParseException

__settings__ = None


def init():
    global __settings__

    with open('settings.conf', 'r') as f:
        __settings__ = json.load(f)


def parse(string, vars, eval=True, gui=False):
    math.set_gui(gui)
    math.set_eval(eval)
    math.set_user_variables(vars)
    if string == "":
        return ml.Empty()
    try:
        if string[0] == '%':
            return text.parse(string[1:])
        else:
            return math.parse(string)
    except ParseException:
        return ml.Variable("ParseException")
