import sys
from subprocess import PIPE, STDOUT, Popen, call
from threading import Thread
from queue import Queue, Empty
import json
import pyperclip
import os
import maple
import latex
from mathlib import *

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


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

    shell_cmd = "java -cp \"{}\" frink.parser.Frink -k "\
        .format(__settings__["frink"])

    frink_proc = Popen(shell_cmd,
                       stdout=PIPE,
                       stdin=PIPE,
                       stderr=STDOUT,
                       universal_newlines=True,
                       shell=True,
                       bufsize=1,
                       close_fds=ON_POSIX)
    # preexec_fn=os.setsid)

    frink_queue = Queue()
    frink_thread = Thread(target=enqueue_output,
                          args=(frink_proc.stdout, frink_queue))
    frink_thread.daemon = True  # thread dies with the program
    frink_thread.start()

    # Catch initial output
    process_input(frink_proc, frink_queue, frink_thread, 20)

    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" ".format(
        __settings__["maple"])

    maple_proc = Popen(shell_cmd,
                       stdout=PIPE,
                       stdin=PIPE,
                       stderr=STDOUT,
                       universal_newlines=True,
                       shell=True,
                       bufsize=1,
                       close_fds=ON_POSIX)
    # preexec_fn=os.setsid)

    maple_queue = Queue()
    maple_thread = Thread(target=enqueue_output,
                          args=(maple_proc.stdout, maple_queue))
    maple_thread.daemon = True  # thread dies with the program
    maple_thread.start()

    # Catch initial output
    process_input(maple_proc, maple_queue, maple_thread, 20)

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
                latex.generate(maple.parse(prompt.strip("mapletolatex"))))
            call(__settings__["pdflatex"] +
                 " -fmt pdflatex mathnotes.tex", shell=True)
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
    return_string = process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)
    return return_string


def maple_query(query_string, proc, queue, thread):
    proc.stdin.write(query_string)
    process_input(proc, queue, thread, 0.5, True)
    return_string = process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print("Return string: " + return_string)
    print_math(maple.parse(return_string))
    return return_string


def process_input(proc, queue, thread, wait=0, single=False):
    try:
        line = queue.get(timeout=wait)  # or q.get(timeout=.1)
    except Empty:
        return ""
    else:  # got line
        if single:
            return line
        else:
            return line + process_input(proc, queue, thread, 0.1)


def generate_latex(output_string):
    output_string = output_string.strip("latex")
    with open("preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)
    with open("mathnotes.tex", "w") as f:
        f.write(output_string)


def print_math(math_list):
    output_string = ""
    for item in math_list:
        if type(item) is list:
            output_string += str(item) + " "
        elif type(item) is Complex:
            output_string += "{} + {}i ".format(item.r, item.i)
        elif type(item) is Root:
            output_string += "sqrt({}, {}) ".format(item.value, item.nth)
        elif type(item) is Power:
            output_string += "{}^({}) ".format(item.value, item.nth)
    print(output_string)
