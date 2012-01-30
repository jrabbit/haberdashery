from subprocess import *
#pip = sys.argv[0]
def is_python():
    pip = Popen(['pip', '--version'], stdout=PIPE).communicate()[0]
    if pip.strip()[-12:].split()[0] == "(python":
        return True