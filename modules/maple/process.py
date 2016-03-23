# maple parser for iEuler
import modules.tools.procio as procio
import modules.maple.parser as parser
import modules.maple.generator as generator

#################
# MAPLE PROCESS #
#################

maple_proc = None
path = None


def evaluate(expr, convert=True):
    global maple_proc
    if maple_proc is None:
        # if not gui_mode:
        # print("Starting Maple...")
        # Spawn Maple subprocess.
        # Returns instance of process, queue and thread for
        # asynchronous I/O
        maple_proc = init()
    return query(expr, *maple_proc, convert=convert)


def set_path(p):
    global path
    path = p


def init():
    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(path)
    return procio.run(shell_cmd)


def query(query, proc, queue, thread, convert=True):
    if convert:
        query = generator.generate(query) + ";\n"
    print("Maple query: {}".format(query))
    proc.stdin.write(query)
    procio.process_input(proc, queue, thread, 0.5, True)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.replace("\n", "")
    print("Maple return string: {}".format(return_string))
    return parser.parse(return_string)
