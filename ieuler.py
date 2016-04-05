import json
import pickle
import modules.ieuler.parser as parser
import modules.ieuler.generator as generator
import modules.latex.generator
import modules.latex.process
import modules.maple.process
import mathlib as ml
import modules.tools.plot2d as plot2d
import modules.tools.transmit as transmit


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

    user_variables = [{}]
    workspace = [{}]
    ans = []
    current_tab = 0

    read_settings()

    gui_mode = False

    # parser.init()
    # modules.latex.process.init()

    if not gui_mode:
        print("Welcome to iEuler v0.1!")

    while True:
        # Parse math string in iEuler syntax to a python representation
        math_string = input("iEuler> ")
        math_obj = parse_math(math_string, ans, user_variables[0], True)
        print(math_obj)
        # Convert to LaTeX
        latex_string = modules.latex.generator.generate(math_obj)
        print("latex: {}".format(latex_string))
        print(modules.ieuler.generator.generate(math_obj))


def console_send_result(command, user_variables):
    result = parser.parse(command, user_variables, True, False)
    print(result)
    print("latex: {}".format(modules.latex.generator.convert_expr(result)))
    print(generator.generate(result))


def gui_send_result(index, command, user_variables, evaluate, workspace):
    result = parser.parse(command, user_variables, evaluate, True)

    if type(result) is ml.Plot:
        plot2d.plot(result)

    latex = modules.latex.generator.convert_expr(result)
    add_to_workspace(workspace, index, command, latex)
    print('{} {}'.format(index, latex))


def add_to_workspace(workspace, index, command, latex):
    workspace[index] = {"command": command, "latex": latex}


def save_workspace(workspace, path):
    f = open(path, 'w')
    for key, value in workspace["user_input"].items():
        f.write(value + "\n")
    f.close()
    f = open(path + "c", 'wb')
    pickle.dump(workspace, f)
    f.close()


def load_workspace(path, tab_index=0):
    f = open(path, 'rb')
    workspace = pickle.load(f)
    f.close
    for key, value in workspace["user_input"].items():
        # tab["user_input"][i] = {"command": line.strip()}
        transmit.send_math_string(tab_index, key, value)
    return workspace


def frink_query(query_string, proc, queue, thread):
    proc.stdin.write(query_string)
    return_string = procio.process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)
    return return_string


def parse_math(math_string, workspace, evaluate):
    return parser.parse(math_string, workspace, evaluate)


def read_settings():
    with open('settings.conf', 'r') as f:
        settings = json.load(f)
    modules.maple.process.set_path(settings["maple"])
    modules.maple.process.set_path(settings["frink"])
    modules.latex.process.set_path(settings["pdflatex"])


def start():
    # Initialize UDP socket
    transmit.init()

    print("Welcome to iEuler v0.1")

    tab_index = 0
    workspace = []

    read_settings()

    while True:
        # Receive data from UDP socket
        cmd, data = transmit.receive()

        if cmd == transmit.PREVIEW or cmd == transmit.EVALUATE:
            tab_index = data["tab_index"]
            index = data["index"]
            math_string = data["math_string"]
            evaluate = cmd == 1

            # Create new tab if it doesn't exist
            if tab_index >= len(workspace):
                workspace.append({})
                workspace[tab_index]["user_variables"] = {}
                workspace[tab_index]["user_input"] = {}
                workspace[tab_index]["user_output"] = {}

            # Parse math string in iEuler syntax to a python representation
            math_obj = parse_math(math_string, workspace[tab_index], evaluate)
            # print(math_obj)

            # Convert to LaTeX
            latex_string = modules.latex.generator.generate(math_obj)

            # Add math object to workspace
            workspace[tab_index]["user_input"][index] = math_string
            workspace[tab_index]["user_output"][index] = latex_string
            workspace[tab_index]["index"] = index

            # Send index and latex string through UDP socket
            transmit.send_latex(tab_index, index, latex_string)
        elif cmd == transmit.OPEN:  # Open workspace
            workspace.append(load_workspace(data["path"], tab_index + 1))
        elif cmd == transmit.SAVE:  # Save workspace
            save_workspace(workspace[tab_index], data["path"])
