from pwn import *

e = ELF("./bookstore")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

p.sendlineafter(":", "1")
p.sendlineafter("book?", "Rocannon's World")
p.sendlineafter("published?", "1966")

p.sendlineafter(":", "3")
p.sendlineafter("book?", "Rocannon's World")
p.sendlineafter("published?", "1966")



gdb.attach(p)

p.interactive()
