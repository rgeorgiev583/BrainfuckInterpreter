__author__ = 'radoslav'
import bfplatform

bfi = bfplatform.create_bfi_stdio_char(
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
)
bfi.run()

bfi = bfplatform.create_bfi_stdio_numeric()
bfi.run()
