# frink module for mathnotes
import procio


def init(path):
    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k preamble.frink "\
        .format(path)
    return procio.run(shell_cmd)
