import socket
import json

ADDRESS = 'localhost'
EULER_PORT = 41000
GUI_PORT = 42000

PREVIEW = 0
EVALUATE = 1
OPEN = 2
SAVE = 3
RENDER = 4
MATH_STR = 5
EXPORT = 6
PLOT = 7
WORKSP = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def init():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ADDRESS, EULER_PORT))


def send_latex(tab_index, index, latex_string):
    data = bytes([RENDER, tab_index, index >> 8, index & 0xFF]) + bytes(
        latex_string, 'utf-8')

    sock.sendto(data, (ADDRESS, GUI_PORT))


def send_math_string(tab_index, index, math_string):
    data = bytes([MATH_STR, tab_index, index >> 8, index & 0xFF]) + bytes(
        math_string, 'utf-8')

    sock.sendto(data, (ADDRESS, GUI_PORT))


def send_plot(tab_index, index, path):
    data = bytes([PLOT, tab_index, index >> 8, index & 0xFF]) + bytes(
        path, 'utf-8')

    sock.sendto(data, (ADDRESS, GUI_PORT))


def send_workspace(tab_index, index, var_lib):
    data = bytes([WORKSP, tab_index, index >> 8, index & 0xFF]) + \
        bytes(json.dumps(var_lib), 'utf-8')

    sock.sendto(data, (ADDRESS, GUI_PORT))


def receive():
    data, addr = sock.recvfrom(1024)
    cmd = data[0]

    if cmd == PREVIEW or cmd == EVALUATE:
        tab_index = data[1]
        index = (data[2] << 8) + (data[3] & 0xFF)
        math_string = data[4:].decode('utf-8')
        result = {
            "tab_index": tab_index,
            "index": index,
            "math_string": math_string
        }
        return (cmd, result)
    elif cmd == OPEN or cmd == SAVE or cmd == EXPORT:
        path = data[1:].decode('utf-8')
        result = {"path": path}
        return (cmd, result)
