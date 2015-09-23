# maple parser for mathnotes
import procio
from mathparser import *


def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def parse(input_string):
    # print("parse({})".format(input_string))
    x = parse_nested(input_string.strip(' '))
    # print("x={}".format(x))
    y = parse_functions(x)
    # print("y={}".format(y))
    z = parse_expression(y)
    print("    result={}".format(z))
    return z
    # return parse_expression(parse_nested(input_string.strip(' ')))
