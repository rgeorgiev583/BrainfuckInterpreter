__author__ = 'radoslav'
import sys
from bfinterpreter import *

# Input/output wrappers for stdin/file/command-line arguments.

'''
    mlinput()

    Function used to enter multi-line data (used for the program input).
    It works like this: you input the data, then append a blank line and after it a line containing a single `.' to
    terminate the input.
'''


def mlinput():
    input_list = []
    input_str = input("> ")

    while not input_str == "." or not input_list[-1] == "":
        input_list.append(input_str)
        input_str = input("> ")

    return input_list

'''
    create_bfi_stdio_numeric(program='')

    Creates and returns a BrainfuckInterpreter initialized with ''program'' (if not, retrieves a brainfuck program from
    the standard input). The interpreter inputs and outputs respectively from the standard input and output, treating
    the data as numbers.
'''


def create_bfi_stdio_numeric(program=''):
    if not program:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(x))

'''
    create_bfi_stdio_char(program='')

    Creates and returns a BrainfuckInterpreter initialized with ''program'' (if not, retrieves a brainfuck program from
    the standard input). The interpreter inputs and outputs respectively from the standard input and output, treating
    the data as characters.
'''


def create_bfi_stdio_char(program=''):
    if not program:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )

'''
    create_bfi_stdio_file_numeric(filename)

    Creates and returns a BrainfuckInterpreter initialized with a brainfuck program retrieved from the file named
    ''filename''. The interpreter inputs and outputs respectively from the standard input and output, treating the data
    as numbers.
'''


def create_bfi_stdio_file_numeric(filename):
    if filename:
        file = open(filename, 'r')
        program = file.read()
        file.close()
    else:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(x))

'''
    create_bfi_stdio_file_char(filename)

    Creates and returns a BrainfuckInterpreter initialized with a brainfuck program retrieved from the file named
    ''filename''. The interpreter inputs and outputs respectively from the standard input and output, treating the data
    as characters.
'''


def create_bfi_stdio_file_char(filename):
    if filename:
        file = open(filename, 'r')
        program = file.read()
        file.close()
    else:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )

'''
    create_bfi_stdio_cli_numeric(program='')

    Creates and returns a BrainfuckInterpreter initialized with ''program'' (if not, retrieves a brainfuck program from
    the first command-line argument). The interpreter inputs and outputs respectively from the standard input and
    output, treating the data as numbers.
'''


def create_bfi_stdio_cli_numeric(program=''):
    if not program:
        program = sys.argv[1]

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(x))

'''
    create_bfi_stdio_cli_char(program='')

    Creates and returns a BrainfuckInterpreter initialized with ''program'' (if not, retrieves a brainfuck program from
    the first command-line argument). The interpreter inputs and outputs respectively from the standard input and
    output, treating the data as characters.
'''


def create_bfi_stdio_cli_char(program=''):
    if not program:
        program = sys.argv[1]

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )
