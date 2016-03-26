from subprocess import PIPE, STDOUT, Popen, call
from threading import Thread
from queue import Queue, Empty
import sys
import re

ON_POSIX = 'posix' in sys.builtin_module_names


def run(cmd, catch=True):
    proc = Popen(cmd,
                 stdout=PIPE,
                 stdin=PIPE,
                 stderr=STDOUT,
                 universal_newlines=True,
                 shell=True,
                 bufsize=1,
                 close_fds=ON_POSIX)

    queue = Queue()
    thread = Thread(target=enqueue_output, args=(proc.stdout, queue))
    thread.daemon = True  # thread dies with the program
    thread.start()

    # Catch initial output
    if catch:
        process_input(proc, queue, thread, 20)
    return (proc, queue, thread)


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


def wait_for_input(proc, queue, thread, regex, timeout=5):
    try:
        line = queue.get(timeout=5)
    except Empty:
        return False
    else:  # got line
        if re.match(regex, line, re.DOTALL):
            return True
        else:
            return wait_for_input(proc, queue, thread, regex, timeout)


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
