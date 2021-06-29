from pwn import *

p = process(["./vmips", "-o", "memsize=2097152", "challenge.rom"])

for i in range(5):
  p.recvuntil("DEBUG::MAC::Process")

print("Sending payload")
for i in range(100):
  p.sendline("s")

p.interactive()
