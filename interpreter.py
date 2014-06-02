__author__ = 'radoslav'


class UnmatchedBracketError(ValueError):
    def __init__(self, pos):
        self.value = pos

    def __str__(self):
        return "The '[' at position {} in the program is unmatched by a ']'.".format(repr(self.pos))


class BrainfuckInterpreter:
    def __init__(self, program='', inputmethod=input, printmethod=print, maxlen_tape=30000, maxsize_cell=256,
                 is_left_unbound=False):
        self.operators = \
        {
            '>': self._next,
            '<': self._prev,
            '+': self._incr,
            '-': self._decr,
            '[': self._loop,
            ']': self._endloop,
            '.': self._put,
            ',': self._get
        }
        self.inputmethod = inputmethod
        self.printmethod = printmethod
        self.maxlen_tape = maxlen_tape
        self.maxsize_cell = maxsize_cell
        self.is_left_unbound = is_left_unbound

        self.program = program
        self._tape = [0]
        self._leftlen_tape = 0
        self._rightlen_tape = 1
        self._dataptr = 0
        self._loopstack = []
        self._iptr = 0

    def _next(self):
        if self.maxlen_tape and self._dataptr == self.maxlen_tape - 1:
            self._dataptr = 0
        else:
            if self._dataptr == self._rightlen_tape - 1:
                self._tape.append(0)
                self._rightlen_tape += 1
            self._dataptr += 1

    def _prev(self):
        if not self.is_left_unbound and self._dataptr == 0 or self.is_left_unbound and self.maxlen_tape and \
                self._dataptr == -self.maxlen_tape:
            self._dataptr = self._rightlen_tape - 1
        else:
            if self.is_left_unbound and self._dataptr == -self._leftlen_tape:
                self._tape.insert(0, 0)
                self._leftlen_tape += 1
            self._dataptr -= 1

    def _incr(self):
        if self._tape[self._dataptr] == self.maxsize_cell - 1:
            self._tape[self._dataptr] = 0
        else:
            self._tape[self._dataptr] += 1

    def _decr(self):
        if self._tape[self._dataptr] == 0:
            self._tape[self._dataptr] = self.maxsize_cell - 1
        else:
            self._tape[self._dataptr] -= 1

    def _loop(self):
        if self._tape[self._dataptr] != 0:
            self._loopstack.append(self._iptr)
        else:
            endpos = self.program.find(']', self._iptr)
            if endpos != -1:
                self._iptr = endpos
            else:
                raise UnmatchedBracketError(self._iptr)

    def _endloop(self):
        if self._tape[self._dataptr] != 0:
            self._iptr = self._loopstack[-1]
        else:
            self._loopstack.pop()

    def _put(self):
        self.printmethod(self._tape[self._dataptr])

    def _get(self):
        self._tape[self._dataptr] = int(self.inputmethod())

    def stepinto(self):
        if self.program[self._iptr] in self.operators:
            self.operators[self.program[self._iptr]]()
        self._iptr += 1

    def tell(self):
        return self._iptr

    def seek(self, newipos):
        self._iptr = newipos

    def run(self):
        while not self._iptr == len(self.program):
            self.stepinto()
