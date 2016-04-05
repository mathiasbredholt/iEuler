# frink module for iEuler
import modules.tools.procio as procio

proc = None
path = None


def init(path):
    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k modules/frink/preamble.frink "\
        .format(path)
    return procio.run(shell_cmd)


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
        query = generator.generate(query) + ";\n"
    print("Frink query: {}".format(query))
    proc.stdin.write(query)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.replace("\n", "")
    print("Frink return string: {}".format(return_string))
    return parser.parse(return_string)
