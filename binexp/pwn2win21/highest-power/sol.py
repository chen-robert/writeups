from pwn import *


def check():
  p = remote("", 8000)
  p.sendline("GET / HTTP/1.0")

  return p.recvline().strip() == "HTTP/1.0 403 Forbidden":
