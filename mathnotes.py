from subprocess import Popen, PIPE, STDOUT

frinkPath = "/Applications/Frink/frink.jar"

def conf():
    f = open('mathnotes.conf', 'w')
    f.write(frinkPath)

def run():
    f = open('mathnotes.conf', 'r')
    frinkPath = f.read()
    print(frinkPath)
    while True:
        prompt = input("> ")
        calc(prompt)

def calc(input):
    cmd = "java -cp {} frink.parser.Frink -e '{}'".format(frinkPath, input);
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True, shell=True)
    print(proc.stdout.readline())
