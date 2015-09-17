import sys
from subprocess import PIPE, STDOUT, Popen, call
from threading import Thread
from queue import Queue, Empty
import json

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def conf(os):
    if os is "win":
        __settings__ = {"frink": "/Applications/Frink/frink.jar",
                        "maple": "/Library/Frameworks/Maple.framework/Versions/2015/bin/maple",
                        "pdflatex": "/usr/texbin/pdflatex"}
    elif os is "osx":
        __settings__ = {"frink": "/Applications/Frink/frink.jar",
                        "maple": "/Library/Frameworks/Maple.framework/Versions/2015/bin/maple",
                        "pdflatex": "/usr/local/texlive/2015/bin/x86_64-darwin/pdftex"}
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

    frink_queue = Queue()
    frink_thread = Thread(target=enqueue_output,
                          args=(frink_proc.stdout, frink_queue))
    frink_thread.daemon = True  # thread dies with the program
    frink_thread.start()

    # Catch initial output
    process_input(frink_proc, frink_queue, frink_thread, 20)

    shell_cmd = " \"{}\" -u -w 0 -c \"interface(prettyprint=0)\" "\
        .format(__settings__["maple"])

    maple_proc = Popen(shell_cmd,
                       stdout=PIPE,
                       stdin=PIPE,
                       stderr=STDOUT,
                       universal_newlines=True,
                       shell=True,
                       bufsize=1,
                       close_fds=ON_POSIX)

    maple_queue = Queue()
    maple_thread = Thread(target=enqueue_output,
                          args=(maple_proc.stdout, maple_queue))
    maple_thread.daemon = True  # thread dies with the program
    maple_thread.start()

    # Catch initial output
    process_input(maple_proc, maple_queue, maple_thread, 20)

    print("Welcome to MathNotes v0.1!")

    while True:
        prompt = input("math> ")
        if "frink" in prompt:
            frink_query(prompt, frink_proc, frink_queue, frink_thread)

        elif "maple" in prompt:
            maple_query(prompt, maple_proc, maple_queue, maple_thread)

        elif "latex" in prompt:
            generate_latex(prompt)

        elif "quit" in prompt:
            print("Killing processes...")
            maple_proc.kill()
            frink_proc.kill()
            print("Quit.")
            break


def frink_query(query_string, proc, queue, thread):
    query_string = query_string.strip("frink")+"\n"
    proc.stdin.write(query_string)
    return_string = process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)


def maple_query(query_string, proc, queue, thread):
    query_string = query_string.strip("maple")+";\n"
    proc.stdin.write(query_string)
    process_input(proc, queue, thread, 0.5, True)
    return_string = process_input(proc, queue, thread, 20)
    return_string = return_string.strip("\n")
    print(return_string)


def process_input(proc, queue, thread, wait=0, single=False):
    try:
        line = queue.get(timeout=wait)  # or q.get(timeout=.1)
    except Empty:
        return ""
    else:  # got line
        if single:
            return line
        else:
            return line + process_input(proc, queue, thread, 0)


def generate_latex(output_string):
    output_string = output_string.strip("latex")
    with open("preamble.tex", "r") as f:
        output_string = f.read().replace("%content", output_string)
    with open("/tmp/mathnotes.tex", "w") as f:
        f.write(output_string)
    call(__settings__["pdflatex"]+" -fmt pdflatex /tmp/mathnotes.tex", shell=True)
