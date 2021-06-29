from pwn import *

p = remote("localhost", 1935)

p.send("\x03")

ui.pause()

p.interactive()
