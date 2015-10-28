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

    user_variables = {}

    parser.init()
    modules.latex.parser.init()

    if not gui_mode:
        print("Welcome to iEuler v0.1!")

    while True:

        do_save = False
        if gui_mode:
            inp = input("")
            if inp == "save":
                path = input("")
                save_worksheet(worksheet, path)
                prompt = None
            elif inp == "load":
                path = input("")
                worksheet = load_worksheet(path)
                prompt = None
            elif inp == "export":
                modules.latex.parser.export(worksheet)
            else:
                index = int(inp)
                evaluate = "evaluate" in input("")
                command = input("")
                if command:
                    gui_send_result(
                        index, command, user_variables, evaluate, worksheet)

        else:
            command = input("iEuler> ")
            console_send_result(command, user_variables)


def console_send_result(command, user_variables):
    result = parser.parse(command, user_variables, True, False)
    print(result)
    print("latex: {}".format(modules.latex.parser.convert_expr(result)))
    print(parser.generate(result))


def gui_send_result(index, command, user_variables, evaluate, worksheet):
    result = parser.parse(command, user_variables, evaluate, True)

    if type(result) is ml.Plot:
        plot2d.plot(result)

    latex = modules.latex.parser.convert_expr(result)
    add_to_worksheet(worksheet, index, command, latex)
    print('{} {}'.format(index, latex))


def add_to_worksheet(worksheet, index, command, latex):
    worksheet[index] = {"command": command, "latex": latex}


def save_worksheet(worksheet, path):
    f = open(path, 'w')
    for key in worksheet:
        f.write(worksheet[key]["command"] + "\n")
    f.close()


def load_worksheet(path, gui_mode=True):
    worksheet = {}
    f = open(path, 'r')
    for i, line in enumerate(f):
        worksheet[i] = {"command": line.strip()}
        print("{} {}".format(i, line.strip()))
    f.close()
    print("Done")
    return worksheet


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
