# frink module for iEuler
import modules.tools.procio as procio


def init(path):
    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k modules/frink/preamble.frink "\
        .format(path)
    return procio.run(shell_cmd)
