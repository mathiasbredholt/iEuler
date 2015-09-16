from subprocess import Popen, PIPE, STDOUT

settings = {"frink": "/Applications/Frink/frink.jar"}

def conf():
    f = open('mathnotes.conf', 'w')
    f.write(settings["frink"])

def run():
    f = open('mathnotes.conf', 'r')
    settings["frink"] = f.read()
    while True:
        prompt = input("> ")
        calc(prompt)

def calc(input):
    cmd = "java -cp {} frink.parser.Frink -e '{}'".format(settings["frink"], input);
    print(cmd)
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True, shell=True)
    print(proc.stdout.readline())
