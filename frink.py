# frink module for mathnotes
import procio


def init(path):
    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k "\
        .format(path)
    return procio.run(shell_cmd)
