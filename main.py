__author__ = 'radoslav'
from interpreter import *
import unittest
import sys


def strip_nops(program):
    return all(op in BrainfuckInterpreter.operators for op in program)


'''
def mlinput():
    try:
        while True:
            data = input("> ")
            if not data:
                break
            yield data
    except KeyboardInterrupt:
        return
'''


def mlinput():
    input_list = []
    input_str = input("> ")

    while not input_str == "." or not input_list[-1] == "":
        input_list.append(input_str)
        input_str = input("> ")

    return input_list


prog = ''.join(mlinput())
bfinterpreter = BrainfuckInterpreter(prog)
    #"++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
#)
bfinterpreter.printmethod = lambda x: sys.stdout.write(str(x))
bfinterpreter.run()
