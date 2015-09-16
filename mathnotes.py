from subprocess import Popen, PIPE, STDOUT

frinkPath = "/Applications/Frink/frink.jar"

def run():
    while True:
        prompt = input("> ")
        calc(prompt)

def calc(input):
    cmd = "java -cp {} frink.parser.Frink -e '{}'".format(frinkPath, input);
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True, shell=True)
    print(proc.stdout.readline())
