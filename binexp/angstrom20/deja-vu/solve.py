from pwn import *

e = ELF("./a_happy_family")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh("team5344", "shell.actf.co", password="4d9ef3c02b7e52dc9ed3")
  p = s.run("/problems/2020/a_happy_family/a_happy_family")
else:
  p = process(e.path)

p.sendlineafter("?", "A" * 32)

p.interactive()
