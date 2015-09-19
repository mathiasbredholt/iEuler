import json
import pyperclip
import os
import maple
import frink
import latex
import mathcmd
from subprocess import call
import procio


def conf(os):
    if os is "win":
        __settings__ = {
            "frink": "C:/Program Files (x86)/Frink/frink.jar",
            "maple": "C:/Program Files/Maple 2015/bin.X86_64_WINDOWS/cmaple",
            "pdflatex": "pdflatex"
        }
    elif os is "osx":
        __settings__ = {
            "frink": "/Applications/Frink/frink.jar",
            "maple":
            "/Library/Frameworks/Maple.framework/Versions/2015/bin/maple",
            "pdflatex": "/usr/local/texlive/2015/bin/x86_64-darwin/pdftex"
        }
    with open('mathnotes.conf', 'w') as f:
        json.dump(__settings__, f)


def run():
    global __settings__

    with open('mathnotes.conf', 'r') as f:
        __settings__ = json.load(f)

    frink_proc, frink_queue, frink_thread = frink.init(__settings__["frink"])
    maple_proc, maple_queue, maple_thread = maple.init(__settings__["maple"])

    preview = []

    print("Welcome to MathNotes v0.1!")

    while True:

        do_save = False
        prompt = input("math> ")

        if ";" in prompt:
            prompt = prompt.strip(";")
            do_save = True

        if "frink" in prompt:
            prompt = prompt.strip("frink") + "\n"
            result_string = frink_query(prompt, frink_proc, frink_queue,
                                        frink_thread)

        elif "maple" in prompt:
            prompt = prompt.strip("maple") + ";\n"
            result_string = maple_query(prompt, maple_proc, maple_queue,
                                        maple_thread)

        elif "maptotex" in prompt:
            generate_latex(
                latex.generate(maple.parse(prompt.strip("maptotex"))))
            call(__settings__["pdflatex"] + " -fmt pdflatex mathnotes.tex",
                 shell=True)
            pyperclip.copy(os.getcwd() + "/mathnotes.pdf")

        elif "latex" in prompt:
            # output_string = ""
            # for item in preview:
            #     output_string += item + "\n"

            # todo
            # generate_latex(latex.generate([Integral(Number("3"), Variable(
            #     "x"), Number("-1"), Number("1")), Root(
            #         Number("2"), Number("4")), Fraction(MulOp(Number(
            #             "2"), Variable(
            #                 "x")), Variable("y")), Derivative(Variable(
            #                     "x"), Variable("y"), Number("2"))]))

            # generate_latex(latex.generate(prompt.strip()))

            call(
                __settings__["pdflatex"] + " -fmt pdflatex mathnotes.tex",
                shell=True)
            pyperclip.copy(os.getcwd() + "/mathnotes.pdf")

        elif "quit" in prompt:
            print("Killing processes...")
            os.killpg(os.getpgid(maple_proc.pid), 15)
            os.killpg(os.getpgid(frink_proc.pid), 15)
            print("Quit.")
            break

        elif ":" in prompt:
            for item in preview:
                print(item)

        else:
            result_string = prompt
            print("Sorry. I don't understand.")

        if do_save:
            preview.append(result_string)


def frink_query(query_string, proc, queue, thread):
    proc.stdin.write(query_string)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)
    return return_string


def maple_query(query_string, proc, queue, thread):
    proc.stdin.write(query_string)
    procio.process_input(proc, queue, thread, 0.5, True)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print("Return string: " + return_string)
    mathcmd.print_math(maple.parse(return_string))
    return return_string


def generate_latex(output_string):
    output_string = output_string.strip("latex")
    with open("preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)
    with open("mathnotes.tex", "w") as f:
        f.write(output_string)
