from pwn import *

e = ELF("./the_office")

context.binary = e

e.asm(0x0804908d, "push 0x1")

e.save("./patched")
