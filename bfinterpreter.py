__author__ = 'radoslav'


# Exception that is thrown when there is an unmatched `]' encountered when executing a brainfuck program
class UnmatchedBracketError(ValueError):
    def __init__(self, pos):
        self.value = pos

    def __str__(self):
        return "The '[' at position {} in the program is unmatched by a ']'.".format(repr(self.pos))


# Obviously, the brainfuck interpreter class
class BrainfuckInterpreter:
    def __init__(self, program='', inputmethod=lambda: int(input()), printmethod=lambda: str(print()),
                 maxlen_tape=30000, maxsize_cell=256, is_left_unbound=False):
        self.operators = \
        {
            '>': self._next,     # `Next cell' operator
            '<': self._prev,     # `Previous cell' operator
            '+': self._incr,     # `Increase value at cell' operator
            '-': self._decr,     # `Decrease value at cell' operator
            '[': self._loop,     # `Loop code between `[' and `]' until value at cell is 0' operator
            ']': self._endloop,  # `End loop' operator
            '.': self._put,      # `Output value at cell' operator
            ',': self._get       # `Input value to cell' operator
        }
        self.inputmethod = inputmethod          # The method used to request data from the user (defaults to ''input'').
        self.printmethod = printmethod          # The method used to display data to the user (defaults to ''input'').
        self.maxlen_tape = maxlen_tape          # Maximum length of the tape.
        self.maxsize_cell = maxsize_cell        # Maximum size of a single cell of the tape.
        self.is_left_unbound = is_left_unbound  # Determines whether the cell should be unbound (extensible) not only to
                                                #   the right but also to the left (i.e. you can append cells to the
                                                #   left)

        self.program = program                  # The brainfuck program to execute.
        self._tape = [0]                        # The tape on which the program operates.
        self._leftlen_tape = 0                  # The length of the tape to the left (i.e. the number of cells to the
                                                #   left of the zero-indexed cell)
        self._rightlen_tape = 1                 # The length of the tape to the right (i.e. the number of cells to the
                                                #   right of the zero-indexed cell including the latter)
        self._dataptr = 0                       # The data pointer: an integer that specifies the position of the
                                                #   current cell of the tape
        self._loopstack = []                    # The loop stack: it contains the positions at which the `['s that
                                                #   correspond to currently running loops are located in the program.
        self._iptr = 0                          # The instruction pointer: an integer that specifies the position at
                                                #   which the currently running brainfuck instruction is located in the
                                                #   program.

    '''
        _next()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Increments (increases by 1) the data pointer (_dataptr).
    '''
    def _next(self):
        if self.maxlen_tape and self._dataptr == self.maxlen_tape - 1:
            self._dataptr = 0
        else:
            if self._dataptr == self._rightlen_tape - 1:
                self._tape.append(0)
                self._rightlen_tape += 1
            self._dataptr += 1

    '''
        _prev()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Decrements (decreases by 1) the data pointer (_dataptr).
    '''
    def _prev(self):
        if not self.is_left_unbound and self._dataptr == 0 or self.is_left_unbound and self.maxlen_tape and \
                self._dataptr == -self.maxlen_tape:
            self._dataptr = self._rightlen_tape - 1
        else:
            if self.is_left_unbound and self._dataptr == -self._leftlen_tape:
                self._tape.insert(0, 0)
                self._leftlen_tape += 1
            self._dataptr -= 1

    '''
        _incr()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Increments (increases by 1) the value at the current cell of the tape.
    '''
    def _incr(self):
        if self._tape[self._dataptr] == self.maxsize_cell - 1:
            self._tape[self._dataptr] = 0
        else:
            self._tape[self._dataptr] += 1

    '''
        _decr()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Decrements (decreases by 1) the value at the current cell of the tape.
    '''
    def _decr(self):
        if self._tape[self._dataptr] == 0:
            self._tape[self._dataptr] = self.maxsize_cell - 1
        else:
            self._tape[self._dataptr] -= 1

    '''
        _loop()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Executes the instructions between `[' and `]', returns to the `[' and then repeats until the value at the
        current cell becomes 0.
    '''
    def _loop(self):
        if self._tape[self._dataptr] != 0:
            self._loopstack.append(self._iptr)
        else:
            endpos = self.program.find(']', self._iptr)
            if endpos != -1:
                self._iptr = endpos
            else:
                raise UnmatchedBracketError(self._iptr)

    '''
        _endloop()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Called when the loop generated by _loop() should end.
    '''
    def _endloop(self):
        if self._tape[self._dataptr] != 0:
            self._iptr = self._loopstack[-1]
        else:
            self._loopstack.pop()

    '''
        _put()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Output the value at the current cell.
    '''
    def _put(self):
        self.printmethod(self._tape[self._dataptr])

    '''
        _get()
        (protected method of BrainfuckInterpreter; not meant to be accessed from outside)

        Input some value to the current cell.
    '''
    def _get(self):
        self._tape[self._dataptr] = self.inputmethod()

    '''
        stepinto()
        (public method of BrainfuckInterpreter)

        Move to the next instruction in the program (increments the _iptr (instruction pointer)).
    '''
    def stepinto(self):
        if self.program[self._iptr] in self.operators:
            self.operators[self.program[self._iptr]]()
        self._iptr += 1

    '''
        tell()
        (public method of BrainfuckInterpreter)

        Returns the value of the _iptr (instruction pointer).
    '''
    def tell(self):
        return self._iptr

    '''
        seek()
        (public method of BrainfuckInterpreter)

        Changes the value of the _iptr (instruction pointer).
    '''
    def seek(self, newipos):
        self._iptr = newipos

    '''
        run()
        (public method of BrainfuckInterpreter)

        Executes the program instruction by instruction.
    '''
    def run(self):
        while not self._iptr == len(self.program):
            self.stepinto()
