__author__ = 'radoslav'

class BrainfuckInterpreter:
    def __init__(self, program):
        self._tape = []
        self._pos = 0
        self._loopstack = []
        self._operators = {
                             '>': self._next,
                             '<': self._prev,
                             '+': self._incr,
                             '-': self._decr,
                             '[': self._loop,
                             ']': self._endloop,
                             '.': self._put,
                             ',': self._get
                        }
        self._ipos = 0
        self.program = program

    def _next(self):
        if self._pos == len(self._tape) - 1:
            self._pos = 0
        else:
            self._pos += 1

    def _prev(self):
        if self._pos == 0:
            self._pos = len(self._tape) - 1
        else:
            self._pos -= 1

    def _incr(self):
        if self._tape[self._pos] == 255:
            self._tape[self._pos] = 0
        else:
            self._tape[self._pos] += 1

    def _decr(self):
        if self._tape[self._pos] == 0:
            self._tape[self._pos] = 255
        else:
            self._tape[self._pos] -= 1

    def _loop(self):
        if self._tape[self._pos] != 0:
            self._loopstack.append(self._ipos)
        else:
            endpos = self.program.find(']')

            if endpos != -1:
                self._ipos = endpos
            else:
                raise Exception()

    def _endloop(self):
        if self._tape[self._pos] != 0:
            _pos = self._loopstack.pop()

    def _put(self, ):
        print(chr(self._tape[self._pos]))

    def _get(self):
        self._tape[self._pos] = ord(input())

    def stepinto(self):
        self._operators[self.program[self._pos]]()

    def step(self):
        if not self._stepovermode:
            self.stepinto()
        else:
            while self.program[self._pos] != ']':
                pos += 1

    def stepover(self):
        self._stepovermode = True


    def runcontinue(self):
        while pos < len(program):

    def tell(self):
        return self.ipos

    def seek(self, newipos):
        self.ipos = newipos

    def run(self, program):


        while not program

