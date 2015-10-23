import json
import modules.ieuler.parser as parser
import modules.latex.parser
import mathlib as ml
import modules.tools.plot2d as plot2d


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
    with open('settings.conf', 'w') as f:
        json.dump(__settings__, f)


def run(argv=None):
    gui_mode = False
    if argv and "-gui" in argv:
        gui_mode = True
        worksheet = {}

    parser.init()
    modules.latex.parser.init()

    if not gui_mode:
        print("Welcome to MathNotes v0.1!")

    while True:

        do_save = False
        if gui_mode:
            index = int(input(""))
            prompt = input("")
            add_to_worksheet(worksheet, index, prompt)
        else:
            prompt = input("math> ")

        if prompt:
            result = parser.parse(prompt)

            if type(result) is ml.Plot:
                plot2d.plot(result)
            else:
                modules.latex.parser.generate(result)

            if gui_mode:
                print(index)
            else:
                print(result)
                print(parser.generate(result))

        # if "print" in prompt:
        #     # print(modules.ieuler.parser.parse(prompt.strip("print")))
        #     print(cmdmath.generate(modules.ieuler.parser.parse(prompt.strip("print"))))

        # elif "frink" in prompt:
        #     if frink_proc is None:
        #         print("Starting Frink...")
        #         # Spawn Frink subprocess.
        #         # Returns instance of process, queue and thread for
        #         # asynchronous I/O
        #         frink_proc, frink_queue, frink_thread = frink.init(
        #             __settings__["frink"])
        #     prompt = prompt.strip("frink") + "\n"
        #     result_string = frink_query(prompt, frink_proc, frink_queue,
        #                                 frink_thread)
        #     if gui_mode:
        #         print(index)
        #     else:
        #         print(cmdmath.generate(modules.maple.parser.parse(result_string)))
        #     # generate_latex(latex.generate(frink.parse(result_string)))
        #     # call(__settings__[
        #     #      "pdflatex"] + " -interaction=batchmode -fmt pdflatex -shell-escape mathnotes.tex", shell=True)

        # elif "maple" in prompt:
        #     if maple_proc is None:
        #         if not gui_mode:
        #             print("Starting Maple...")
        #         # Spawn Maple subprocess.
        #         # Returns instance of process, queue and thread for
        #         # asynchronous I/O
        #         maple_proc, maple_queue, maple_thread = modules.maple.parser.init(
        #             __settings__["maple"])
        #     prompt = prompt.strip("maple") + ";\n"
        #     try:
        #         result_string = maple_query(prompt, maple_proc, maple_queue,
        #                                     maple_thread)
        #     except:
        #         print("Timeout")
        #     else:
        #         latex.generate(modules.maple.parser.parse(result_string), __settings__)
        #         if gui_mode:
        #             print(index)
        #         else:
        #             print(cmdmath.generate(modules.maple.parser.parse(result_string)))

        #     # print(cmdmath.generate(modules.maple.parser.parse(result_string)))

        # elif "latex" in prompt:
        #     latex.generate(modules.maple.parser.parse(
        #         prompt.strip("latex")), __settings__)
        #     if gui_mode:
        #         print(index)
        #     else:
        #         print(cmdmath.generate(modules.maple.parser.parse(result_string)))

        #     # pyperclip.copy(os.getcwd() + "/mathnotes.pdf")

        # elif "plot" in prompt:
        #     plot2d.plot(modules.maple.parser.parse(prompt.strip("plot")))
        #     if gui_mode:
        #         print(index)
        # elif "quit" in prompt:
        #     print("Killing processes...")
        #     os.killpg(os.getpgid(maple_proc.pid), 15)
        #     os.killpg(os.getpgid(frink_proc.pid), 15)
        #     print("Quit.")
        #     break

        # else:
        #     result_string = prompt
        #     print("Sorry. I don't understand: \"{}\"".format(prompt))


def add_to_worksheet(worksheet, index, command):
    worksheet[index] = {"command": command}


def frink_query(query_string, proc, queue, thread):
    proc.stdin.write(query_string)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)
    return return_string


# def generate_latex(output_string):
#     with open("modules/latex/preamble.tex", "r") as f:
#         output_string = f.read().replace("%content", output_string)
#     with open("mathnotes.tex", "w") as f:
#         f.write(output_string)
