__author__ = 'radoslav'
# Numeric console input/output wrapper


def mlinput():
    input_list = []
    input_str = input("> ")

    while not input_str == "." or not input_list[-1] == "":
        input_list.append(input_str)
        input_str = input("> ")

    return input_list

class ConsoleNumericIO:
    def __init__(self, bfi):
        self.bfi = bfi
        bfi.inputmethod =

