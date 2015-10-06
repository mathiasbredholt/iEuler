# maple parser for mathnotes
import procio
from mathparser import *


def init(path):
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def parse(input_string):
    x = parse_expression(input_string.strip(' '))
    return x
