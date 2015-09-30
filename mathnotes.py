import json
# import pyperclip
import os
import maple
import frink
import latex
import cmdmath
from subprocess import call, PIPE
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


def run(input_string=None):
    global __settings__

    with open('mathnotes.conf', 'r') as f:
        __settings__ = json.load(f)

    maple_proc = None
    frink_proc = None

    if input_string:
        generate_latex(latex.generate(maple.parse(input_string)))
        call(__settings__["pdflatex"] +
             " -interaction=batchmode -fmt pdflatex -shell-escape mathnotes.tex",
             shell=True)
    else:
        preview = []
        print("Welcome to MathNotes v0.1!")

        while True:

            do_save = False
            prompt = input("math> ")

            if "print" in prompt:
                print(cmdmath.generate(maple.parse(prompt.strip("print"))))

            elif ";" in prompt:
                prompt = prompt.strip(";")
                do_save = True

            elif "frink" in prompt:
                if frink_proc is None:
                    print("Starting Frink...")
                    # Spawn Frink subprocess.
                    # Returns instance of process, queue and thread for
                    # asynchronous I/O
                    frink_proc, frink_queue, frink_thread = frink.init(
                        __settings__["frink"])
                prompt = prompt.strip("frink") + "\n"
                result_string = frink_query(prompt, frink_proc, frink_queue,
                                            frink_thread)
                # generate_latex(latex.generate(frink.parse(result_string)))
                # call(__settings__[
                #      "pdflatex"] + " -interaction=batchmode -fmt pdflatex -shell-escape mathnotes.tex", shell=True)

            elif "maple" in prompt:
                if maple_proc is None:
                    if not gui_mode:
                        print("Starting Maple...")
                    # Spawn Maple subprocess.
                    # Returns instance of process, queue and thread for
                    # asynchronous I/O
                    maple_proc, maple_queue, maple_thread = maple.init(
                        __settings__["maple"])
                prompt = prompt.strip("maple") + ";\n"
                result_string = maple_query(prompt, maple_proc, maple_queue,
                                            maple_thread)
                latex.generate(maple.parse(result_string))
                print(result_string)

                # print(cmdmath.generate(maple.parse(result_string)))

            elif "latex" in prompt:
                latex.generate(maple.parse(prompt.strip("latex")))
                print(result_string)
                # pyperclip.copy(os.getcwd() + "/mathnotes.pdf")

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
                print("Sorry. I don't understand: \"{}\"".format(prompt))

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
    print("    Return string: " + return_string)
    cmdmath.convert_expr(maple.parse(return_string))
    return return_string


# def generate_latex(output_string):
#     with open("preamble.tex", "r") as f:
#         output_string = f.read().replace("%content", output_string)
#     with open("mathnotes.tex", "w") as f:
#         f.write(output_string)
