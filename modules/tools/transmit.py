import socket

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
NEW = 7

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ADDRESS, EULER_PORT))
    server.listen(1)


def send_latex(tab_index, index, latex_string):
    data = bytes([RENDER, tab_index, index >> 8, index & 0xFF]) + bytes(
        latex_string, 'utf-8')
    server.send(data)


def send_math_string(tab_index, index, math_string):
    data = bytes([MATH_STR, tab_index, index >> 8, index & 0xFF]) + bytes(
        math_string, 'utf-8')
    server.send(data)


def receive():
    # data, addr = server.recvfrom(1024)
    data, addr = [10], 0
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
    elif cmd == OPEN or cmd == SAVE:
        path = data[1:].decode('utf-8')
        result = {"path": path}
        return (cmd, result)
    else:
        return (cmd, {})

# Test input
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(('localhost', 41000))
# while 1:
#     data, addr = s.recvfrom(1024)
#     print(data)
