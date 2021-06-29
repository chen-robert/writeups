from pwn import *

e = ELF("./heap")

context.binary = e.path

s = ssh(host="ctf.villageidiotlabs.org", user="user", password="showmethemips", port=2222)
p = s.run("/home/user/heap")


p.interactive()
