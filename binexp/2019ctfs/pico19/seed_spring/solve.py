from pwn import *
import ctypes

e = ELF("./seed_spring")
context.binary = e.path

if "--remote" in sys.argv:
  p = remote("2019shell1.picoctf.com", 32233)
else:
  p = process(e.path
  )
timer = process("./a.out")

p.recvuntil(":")
p.sendline(str(int(timer.recvline()) & 0xf))



p.interactive()
