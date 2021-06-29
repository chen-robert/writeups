from pwn import *

r = process("./concrete_trap")
r.send(b'u_will_never_guess_this_because_its_so_long\n16690 51\n3827302487 2572191808 2063707744 0073308775 1132333216\n')

r.interactive()
