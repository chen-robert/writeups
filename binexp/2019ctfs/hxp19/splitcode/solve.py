from pwn import *

e = ELF("./vuln")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

gdb.attach(p)

p.sendline(
  (
    asm("""

    """)
  ).ljust(0x2a, "\x00")

)

p.interactive()
