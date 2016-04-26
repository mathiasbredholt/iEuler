
import modules.tools.procio as procio
import modules.latex.generator as generator
import json

path = None


def set_path(p):
    global path
    path = p


# generates LaTeX string from mathlib operators
def generate_preview(input_expr):
    output_string = generator.convert_expr(input_expr)
    with open("modules/latex/preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)
    with open("mathnotes.tex", "w") as f:
        f.write(output_string)

    proc, queue, thread = procio.run(
        path +
        " -interaction=batchmode -fmt pdflatex -shell-escape mathnotes.tex",
        False)
    proc.wait()
    proc, queue, thread = procio.run(
        "convert -density 300 mathnotes.pdf mathnotes.png", False)
    proc.wait()
    return output_string


def export(worksheet):
    output_string = ""
    for index, value in worksheet["latex_output"].items():
        output_string = output_string + "$$" + value + "$$\\\\"

    with open("modules/latex/preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)

    with open("output.tex", "w") as f:
        f.write(output_string)

    proc, queue, thread = procio.run(
        path + " -interaction=batchmode -fmt pdflatex output.tex",
        False)
    proc.wait()
