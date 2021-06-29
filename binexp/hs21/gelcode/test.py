from pwn import *

e = ELF("./chal")

context.binary = e

for i in range(0x10):
  for j in range(0x10):
    for k in range(0x10):
      for k2 in range(0x10):
        print(disasm(chr(i) + chr(j) + chr(k) + chr(k2)))

