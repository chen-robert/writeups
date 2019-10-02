from pwn import *

p = process("./T1_crackme")
p = remote("rev.chal.csaw.io", 1003)

p.recvuntil("?")
p.sendline(chr(0x6c) + chr(0x4f) + chr(0x6c) + chr(0x54) + chr(0x79) + chr(0x4c) + chr(0x65) + chr(0x52) + chr(0x31))

goal = 0x100000008
a = 0x7fffffff
p.sendline(str(a))
p.sendline(str(a))
p.sendline(str(goal - a * 2))

nums = [0x42, 0x62, 0x6c, 0x6f, 0x6f, 0x30, 0x30, 0x30, 0x64, 0x64, 0x64, 0x44, 0x5f, 0x5f, 0x52, 0x75, 0x75, 0x73, 0x68, 0x21]

ret = ""
for i in nums:
  ret += chr(i)
p.sendline(ret)

p.interactive()
