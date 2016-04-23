# frink module for iEuler
import modules.tools.procio as procio
import modules.frink.parser as parser
import modules.frink.generator as generator

proc = None
path = None


def init():
    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k modules/frink/preamble.frink "\
        .format(path)
    print(shell_cmd)
    return procio.run(shell_cmd, catch=True)


def set_path(p):
    global path
    path = p


def evaluate(expr, convert=True):
    global proc
    if proc is None:
        proc = init()
    return query(expr, *proc, convert=convert)


def query(query, proc, queue, thread, convert=True):
    if convert:
        query = generator.generate(query) + "\n"
    print("Frink query: {}".format(query))
    proc.stdin.write(query)
    print(query)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.replace("\n", "")
    print("Frink return string: {}".format(return_string))
    return parser.parse(return_string)
