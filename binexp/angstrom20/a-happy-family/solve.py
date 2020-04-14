from pwn import *
import random

p = process("./a_happy_family")

def rev(s):
  code = "angstromctf20"
  ret = 0
  for i in range(len(s)):
    if random.randint(0, 1) == 0:
      ret += code.index(s[i])
    else:
      ret += code.rfind(s[i])
    ret *= 13
  return ret / 13

def to_base(n):
  code = "angstromctf20"
  s = ""
  for i in range(18):
    s = code[n % 13] + s
    n //= 13

  return s

def valid(s):
  return all(c in string.printable for c in s)

offset = 13**18

c1 = "\x00"
c2 = "\x00"
c3 = "\x00"
c4 = "\x00"

while not valid(c1):
  c1 = p64(rev("artomtf2srn00tgm2f"))
while not valid(c2):
  c2 = p64((0x100**8) + (~rev("ng0fa0mat0tmmmra0c")))

while not valid(c3):
  c3 = p64(0x100**8 - (rev("ngnrmcornttnsmgcgr") - 0x1337))
while not valid(c4):
  c4 = p64(0x1234567890abcdef ^ (rev("a0fn2rfa00tcgctaot") + 0x4242))

print(c1)
print(c2)

print(c3)
print(c4)

ret = ""

for i in range(len(c1)):
  ret += c1[i]
  ret += c3[i]

for i in range(len(c2)):
  ret += c2[i]
  ret += c4[i]

print(ret)
p.send(ret)

p.interactive()
