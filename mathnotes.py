import json
# import pyperclip
import os
import maple
import frink
import latex
import cmdmath
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


def run(argv=None):
    gui_mode = False
    if argv and "-gui" in argv:
        gui_mode = True
        worksheet = {}

    global __settings__

    with open('mathnotes.conf', 'r') as f:
        __settings__ = json.load(f)

    maple_proc = None
    frink_proc = None

    preview = []

    if not gui_mode:
        print("Welcome to MathNotes v0.1!")

    while True:

        do_save = False
        if not gui_mode:
            prompt = input("math> ")
        else:
            index = int(input(""))
            prompt = input("")
            add_to_worksheet(worksheet, index, prompt)

        if "print" in prompt:
            print(cmdmath.generate(maple.parse(prompt.strip("print"))))

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
            print(index)
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
            try:
                result_string = maple_query(prompt, maple_proc, maple_queue,
                                            maple_thread)
            except:
                print("Timeout")
            else:
                latex.generate(maple.parse(result_string), __settings__)
                print(index)

            # print(cmdmath.generate(maple.parse(result_string)))

        elif "latex" in prompt:
            latex.generate(maple.parse(prompt.strip("latex")), __settings__)
            print(index)
            # pyperclip.copy(os.getcwd() + "/mathnotes.pdf")

        elif "quit" in prompt:
            print("Killing processes...")
            os.killpg(os.getpgid(maple_proc.pid), 15)
            os.killpg(os.getpgid(frink_proc.pid), 15)
            print("Quit.")
            break

        else:
            result_string = prompt
            print("Sorry. I don't understand: \"{}\"".format(prompt))

        if do_save:
            preview.append(result_string)


def add_to_worksheet(worksheet, index, command):
    worksheet[index] = {"command": command}


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
    # print("    Return string: " + return_string)
    cmdmath.convert_expr(maple.parse(return_string))
    return return_string

# def generate_latex(output_string):
#     with open("preamble.tex", "r") as f:
#         output_string = f.read().replace("%content", output_string)
#     with open("mathnotes.tex", "w") as f:
#         f.write(output_string)
