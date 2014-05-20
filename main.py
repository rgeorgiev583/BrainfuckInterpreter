__author__ = 'radoslav'
from interpreter import *
import sys

bfinterpreter = BrainfuckInterpreter(
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
)
bfinterpreter.printmethod = lambda x: sys.stdout.write(chr(x))
bfinterpreter.run()
