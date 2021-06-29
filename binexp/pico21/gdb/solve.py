import gdb

gdb.execute("file brute")
gdb.execute("set disable-randomization on")
gdb.execute("b *0x5655599b")


while True:
  gdb.execute("r")

  for i in range(len("picoCTF{I")):
    gdb.execute("c")
  
  try:
    gdb.execute("c")

    break
  except Exception:
    pass


print("DONE")
