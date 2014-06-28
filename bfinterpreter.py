__author__ = 'radoslav'


class UnmatchedBracketError(ValueError):
    """
    UnmatchedBracketError() -> There is an unmatched `]' encountered when executing a brainfuck program.
    """
    def __init__(self, pos):
        self.value = pos

    def __str__(self):
        return "The '[' at position {} in the program is unmatched by a ']'.".format(repr(self.pos))


class BrainfuckInterpreter:
    # The brainfuck interpreter class. Use it to create an interpreter for a specific brainfuck program with the given
    # options (IO methods and size constraints).

    def __init__(self, program='', inputmethod=lambda: int(input()), printmethod=lambda x: str(print(x)),
                 maxlen_tape=30000, maxsize_cell=256, is_left_unbound=False,
                 operator_tokens=('>', '<', '+', '-', '[', ']', '.', ',')):
        """
        BrainfuckInterpreter() -> new brainfuck interpreter initialized without a program, using ''int(input())'' for
        input method and ''str(print(x))'' (where `x' is the thing to print) for output method, with maximum tape length
        of 30000 (30000 to the left and the same amount to the right), maximum cell size of 256 (as in 256 different
        values), left-boundedness and using the default brainfuck operator lexical symbols (as opposed to a brainfuck
        dialect (aka isomorph)).
        BrainfuckInterpreter(program='', inputmethod=lambda: int(input()), printmethod=lambda x: str(print(x)),
        maxlen_tape=30000, maxsize_cell=256, is_left_unbound=False,
        operator_tokens=('>', '<', '+', '-', '[', ']', '.', ','))) -> new brainfuck interpreter initialized with
        ''program'' with the given options as subsequent arguments.
        """
        default_tokens = ('>', '<', '+', '-', '[', ']', '.', ',')
        if operator_tokens != default_tokens:
            for (i, token) in enumerate(operator_tokens):
                program.replace(token, default_tokens[i])

        """ Brainfuck operators """
        self.operators = \
        {
            '>': self._next,     # ``Go to next cell'' operator
            '<': self._prev,     # ``Go to previous cell'' operator
            '+': self._incr,     # ``Increment value at current cell'' operator
            '-': self._decr,     # ``Decrement value at current cell'' operator
            '[': self._loop,     # ``Loop code between `[' and `]' until value at current cell is 0'' operator
            ']': self._endloop,  # ``End of loop'' operator
            '.': self._put,      # ``Output value at cell'' operator
            ',': self._get       # ``Input value to cell'' operator
        }
        """ Method used to request data from the user (defaults to ''lambda: int(input())''). """
        self.inputmethod = inputmethod
        """ Method used to display data to the user (defaults to ''lambda x: str(print(x))''). """
        self.printmethod = printmethod
        """ Maximum length of the tape. """
        self.maxlen_tape = maxlen_tape
        """ Maximum size of a single cell of the tape. """
        self.maxsize_cell = maxsize_cell
        """ Determines whether the tape should be unbound (extensible) not only to the right but also to the left
            (so that you could be able to append cells to the left). """
        self.is_left_unbound = is_left_unbound
        """ The brainfuck program to execute. """
        self.program = program
        """ The tape on which the program operates. """
        self._tape = [0]
        """ Length of the tape to the left (i.e. the number of cells to the left of the zero-indexed cell). """
        self._leftlen_tape = 0
        """ Length of the tape to the right (i.e. the number of cells to the right of the zero-indexed cell including
            the latter).
        """
        self._rightlen_tape = 1
        """ The data pointer: an integer that specifies the position of the current cell on the tape. """
        self._dataptr = 0
        """ The loopstack: list of the positions in the code of the opening brackets of the currently running loops
            ordered by their nesting level. """
        self._loopstack = []
        """ The instruction pointer: an integer that specifies the position at which the currently running brainfuck
            instruction is located in the program. """
        self._iptr = 0

    def _next(self):
        """
        _next()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Increment (increase by 1) the data pointer (_dataptr).
        """
        if self.maxlen_tape and self._dataptr == self.maxlen_tape - 1:
            self._dataptr = 0
        else:
            if self._dataptr == self._rightlen_tape - 1:
                self._tape.append(0)
                self._rightlen_tape += 1
            self._dataptr += 1

    def _prev(self):
        """
        _prev()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Decrement (decrease by 1) the data pointer (_dataptr).
        """
        if not self.is_left_unbound and self._dataptr == 0 or self.is_left_unbound and self.maxlen_tape and \
                self._dataptr == -self.maxlen_tape:
            self._dataptr = self._rightlen_tape - 1
        else:
            if self.is_left_unbound and self._dataptr == -self._leftlen_tape:
                self._tape.insert(0, 0)
                self._leftlen_tape += 1
            self._dataptr -= 1

    def _incr(self):
        """
        _incr()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Increment (increase by 1) the value at the current cell of the tape.
        """
        if self._tape[self._dataptr] == self.maxsize_cell - 1:
            self._tape[self._dataptr] = 0
        else:
            self._tape[self._dataptr] += 1

    def _decr(self):
        """
        _decr()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Decrement (decrease by 1) the value at the current cell of the tape.
        """
        if self._tape[self._dataptr] == 0:
            self._tape[self._dataptr] = self.maxsize_cell - 1
        else:
            self._tape[self._dataptr] -= 1

    def _loop(self):
        """
        _loop()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Execute the instructions between `[' and `]', return to the `[' and then repeat until the value at the
        current cell becomes 0.
        """
        if self._tape[self._dataptr] != 0:
            self._loopstack.append(self._iptr)
        else:
            endpos = self.program.find(']', self._iptr)
            if endpos != -1:
                self._iptr = endpos
            else:
                raise UnmatchedBracketError(self._iptr)

    def _endloop(self):
        """
        _endloop()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Called when the loop generated by _loop() ends.
        """
        if self._tape[self._dataptr] != 0:
            self._iptr = self._loopstack[-1]
        else:
            self._loopstack.pop()

    def _put(self):
        """
        _put()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Output the value at the current cell.
        """
        self.printmethod(self._tape[self._dataptr])


    def _get(self):
        """
        _get()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Input some value into the current cell.
        """
        self._tape[self._dataptr] = self.inputmethod()


    def stepinto(self):
        """
        stepinto()
        (public method of BrainfuckInterpreter)

        Move to the next instruction in the program (by incrementing the _iptr (instruction pointer)).
        """
        if self.program[self._iptr] in self.operators:
            self.operators[self.program[self._iptr]]()
        self._iptr += 1

    def tell(self):
        """
        tell() -> integer
        (public method of BrainfuckInterpreter)

        Return the value of the _iptr (instruction pointer).
        """
        return self._iptr

    def seek(self, newipos):
        """
        seek(newipos)
        (public method of BrainfuckInterpreter)

        Change the value of the _iptr (instruction pointer) to the value of `newipos'.
        """
        self._iptr = newipos

    def run(self):
        """
        run()
        (public method of BrainfuckInterpreter)

        Execute the program instruction by instruction.
        """
        while not self._iptr == len(self.program):
            self.stepinto()
