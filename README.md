BRAINFUCK INTERPRETER v0.1
==========================

Last revision: May 19, 2014
Copyright (C) 2014 Radoslav Georgiev
Licensed under the GNU GPL v3


The brainfuck programming language
==================================

(Please see the relevant Wikipedia article for brainfuck:
<https://en.wikipedia.org/wiki/Brainfuck>.
You could also take a look at the relevant Esolangs article,
<http://esolangs.org/wiki/Brainfuck>, for a more detailed outlook on the
specifics of the language.)

brainfuck is a minimalistic esoteric programming lanuguage noted for its
extremely small number of instructions and its extremely small compiler
size (with the smallest known compiler being 100 bytes in size).
It consists of only eight commands and an instruction pointer.
It is completely impractical to implement anything in, making it useful
only for challenging savvy programmers and questioning the fringes of
programming concepts and paradigms.

More specifically, brainfuck is a Turing tarpit, trying to emulate the
Turing machine's instruction set as close as possible, offering the same
computational ability as any other Turing-complete programming language
but at the price of non-intuitiveness, being slow, wasting space, and
being generally difficult to program in.


Overview
--------

The language consists of eight commands. A brainfuck program is a
sequence of these commands, possibly interspersed with other characters
(which are ignored). The commands are executed sequentially, with some
exceptions: an instruction pointer begins at the first command, and each
command it points to is executed, after which it normally moves forward
to the next command. The program terminates when the instruction pointer
moves past the last command.


Brainfuck's virtual machine
---------------------------

The brainfuck language uses a simple machine model consisting of the
program and an instruction pointer; as well as a tape (usually
implemented as an array/vector or a list) of (usually at least 30,000)
cells (usually one byte in width but can also be of larger widths) each
one storing an integer initialized to zero. It also includes a movable
data pointer (initialized to point to the leftmost cell of the tape)
that points to the tape cell which is currently being operated on; and
two streams for input and output (usually using the ASCII character
encoding).


Commands
--------

Brainfuck comprises eight commands, none of which take any parameters:

>  increments (increases by one) the data pointer
   (to point to the next cell to the right).
<  decrements (decreases by one) the data pointer
   (to point to the next cell to the left).
+  increments the byte at the data pointer.
-  decrements the byte at the data pointer.
.  outputs the value (integer) at the data pointer.
,  accepts one integer of input, storing its value in the cell at the
   data pointer.
[  jumps the instruction pointer forward to the command after the
   matching ] command if the byte at the data pointer is zero
   (instead of moving the instruction pointer forward to the next
   command).
]  jumps the instruction pointer back to the command after the matching
   [ command if the byte at the data pointer is nonzero
   (instead of moving the instruction pointer forward to the next
   command).

NOTE: [ and ] match just like ordinary brackets do: for each [ there
must be a corresponding ] in the program. If there is an unmatched [,
the interpreter will raise a syntax error.

These commands can be translated to the following C statements:

NOTE: It is assumed that the C program includes these definitions:
<code language="C">
#include <stddef.h>
const size_t MAX_SIZE = 30000; // tape size constraints;
                                  quantity is the minimum; can be more
char tape[MAX_SIZE] = {}; // the tape from the language's VM;
                             filled with zeroes
char *dptr = tape;   // the data pointer from the language's VM
</code>

>  ++dptr;
<  --dptr;
+  ++*dptr;
-  --*dptr;
.  putchar(*dptr);
,  *dptr = getchar();
[  while (*dptr) {
]  }

Specifics
---------


As the name suggests, brainfuck programs tend to be difficult to
comprehend. This is partly because any mildly complex task requires a
long sequence of commands; partly it is because the program's text gives
no direct indications of the program's state. These, as well as
brainfuck's inefficiency and its limited input/output capabilities, are
some of the reasons it is not used for serious programming. Nonetheless,
like any Turing-complete language, brainfuck is theoretically capable of
computing any computable function or simulating any other computational
model, if given access to an unlimited amount of memory. A variety of
brainfuck programs have been written. Although brainfuck programs,
specially complicated ones, are difficult to write, it is quite trivial
to write an interpreter for brainfuck in a more typical language such as
C due to its simplicity. There even exists a brainfuck interpreter
written in the brainfuck language itself.


The brainfuck Interpreter
=========================


Features
--------

For now none of any importance, apart from accepting a brainfuck program
from stdin or from a file as input.

Possible suggestions for future releases (milestones):
- definition of spatial and temporal constraints on the language's VM
- pbrain (procedural brainfuck) extensions support
- ...and even support of brainfuck dialects!


Usage
-----


For now, the program offers a minimal command-line interface: it accepts
the brainfuck program as a command-line argument and writes the output
of its execution to the standard output.

There are plans for making an interactive console app or even a GUI one.

