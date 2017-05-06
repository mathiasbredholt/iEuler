import sublime
import sublime_plugin
import queue
import os
# import iEuler.modules.pexpect.pexpect as pexpect

import iEuler.modules.tools.procio as procio
import iEuler.modules.ieuler.parser as parser
import iEuler.modules.ieuler.generator as euler_generator
import iEuler.modules.latex.generator as latex_generator

path = sublime.packages_path() + "/iEuler"

workspace = {}
workspace["user_variables"] = {}
workspace["raw_input"] = {}
workspace["parsed_input"] = {}
workspace["latex_output"] = {}
workspace["default_calculator"] = "maple"

mathematical = None


class EulerEventListener(sublime_plugin.ViewEventListener):

    def __init__(self, view):
        self.view = view
        self.phantoms = []

    def on_modified_async(self):
        global mathematical

        region = self.view.sel()[0]
        math_string = self.view.substr(self.view.line(region))

        math_obj = parser.parse(math_string, workspace, True)
        latex_string = latex_generator.generate(math_obj)

        # print("Latex: ", latex_string)

        # if mathematical is None:
        #     cmd = "'" + path + "/modules/mathematical/render.rb'"
        #     mathematical = pexpect.spawn(cmd)

        # mathematical.sendline(latex_string)

        # while True:
        #     try:
        #         data = mathematical.read_nonblocking(size=2000, timeout=1000)
        #     except pexpect.TIMEOUT:
        #         break

        # data = data.replace("\n", "")
        # data = data.replace("\r", "")
        # data = data.replace("\"", "")

        # print(data)

        # (proc, queue, thread) = procio.run(
        #     os.getcwd() + '/modules/mathematical/render.rb', False)
        # proc.kill()

        html = "<div style='background-color:white; padding: 1em; color: black'>{}</div>".format(
            latex_string)

        # html = "<div style='background-color:white; padding: 1em;'><img src=\"{}\"></div>".format(
        #     "data:image/png;base64," + data)

        (row, col) = self.view.rowcol(region.begin())

        self.view.erase_phantoms("eq" + str(row))

        self.view.add_phantom("eq" + str(row), region,
                              html, sublime.LAYOUT_BLOCK)

    @classmethod
    def is_applicable(cls, settings):
        syntax = settings.get('syntax')
        return syntax == 'Packages/iEuler/iEuler.sublime-syntax'

    @classmethod
    def applies_to_primary_view_only(cls):
        return True
