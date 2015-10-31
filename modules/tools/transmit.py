import socket

ADDRESS = 'localhost'
EULER_PORT = 41000
GUI_PORT = 42000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def init():
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind((ADDRESS, EULER_PORT))


def send_latex(index, latex_string):
    cmd = 4  # Render
    data = bytes([cmd, index >> 8, index & 0xFF]) + bytes(latex_string,
                                                          'utf-8')

    client_socket.sendto(data, (ADDRESS, GUI_PORT))


def send_math_string(index, math_string):
    cmd = 5  # Load
    data = bytes([cmd, index >> 8, index & 0xFF]) + bytes(math_string, 'utf-8')

    client_socket.sendto(data, (ADDRESS, GUI_PORT))


def receive():
    data, addr = client_socket.recvfrom(1024)
    cmd = data[0]

    if cmd == 0 or cmd == 1:  # Preview or eval
        index = (data[1] << 8) + (data[2] & 0xFF)
        math_string = data[3:].decode('utf-8')
        result = {"index": index, "math_string": math_string}
        return (cmd, result)
    elif cmd == 2 or cmd == 3:  # Open or save
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
