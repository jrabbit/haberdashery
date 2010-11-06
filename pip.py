from subprocess import *
import sys
#pip = sys.argv[0]
def is_python():
    pip = Popen(['pip', '--version'], stdout=PIPE).communicate()[0]
    if pip[-12:].split() == "(python":
        return True