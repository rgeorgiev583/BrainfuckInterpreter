__author__ = 'radoslav'
import sys
from bfinterpreter import *

# Input/output wrappers for stdin/file/command-line arguments.

def mlinput():
    """
    mlinput() -> list of strings

    Enter multi-line data (used for the program input).
    It works like this: you input the data, then append a blank line and after it a line containing a single `.' to
    terminate the input.
    """
    input_list = []
    input_str = input("> ")

    while not input_str == "." or not input_list[-1] == "":
        input_list.append(input_str)
        input_str = input("> ")

    return input_list


def create_bfi_stdio_numeric(program=''):
    """
    create_bfi_stdio_numeric(program='') -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with ''program'' (if not, retrieve a brainfuck program from
    the standard input). The interpreter inputs and outputs respectively from the standard input and output, treating
    the data as numbers.
    """
    if not program:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(str(x)))


def create_bfi_stdio_char(program=''):
    """
    create_bfi_stdio_char(program='') -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with ''program'' (if not, retrieve a brainfuck program from
    the standard input). The interpreter inputs and outputs respectively from the standard input and output, treating
    the data as characters.
    """
    if not program:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )


def create_bfi_stdio_file_numeric(filename):
    """
    create_bfi_stdio_file_numeric(filename) -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with a brainfuck program retrieved from the file named
    ''filename''. The interpreter inputs and outputs respectively from the standard input and output, treating the data
    as numbers.
    """
    if filename:
        file = open(filename, 'r')
        program = file.read()
        file.close()
    else:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(str(x)))


def create_bfi_stdio_file_char(filename):
    """
    create_bfi_stdio_file_char(filename) -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with a brainfuck program retrieved from the file named
    ''filename''. The interpreter inputs and outputs respectively from the standard input and output, treating the data
    as characters.
    """
    if filename:
        file = open(filename, 'r')
        program = file.read()
        file.close()
    else:
        program = ''.join(mlinput())

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )


def create_bfi_stdio_cli_numeric(program=''):
    """
    create_bfi_stdio_cli_numeric(program='') -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with ''program'' (if not, retrieve a brainfuck program from
    the first command-line argument). The interpreter inputs and outputs respectively from the standard input and
    output, treating the data as numbers.
    """
    if not program:
        program = sys.argv[1]

    return BrainfuckInterpreter(program, printmethod=lambda x: sys.stdout.write(str(x)))


def create_bfi_stdio_cli_char(program=''):
    """
    create_bfi_stdio_cli_char(program='') -> BrainfuckInterpreter

    Create and return a BrainfuckInterpreter initialized with ''program'' (if not, retrieve a brainfuck program from
    the first command-line argument). The interpreter inputs and outputs respectively from the standard input and
    output, treating the data as characters.
    """
    if not program:
        program = sys.argv[1]

    return BrainfuckInterpreter(
        program, inputmethod=lambda: ord(input()), printmethod=lambda x: sys.stdout.write(chr(x))
    )
