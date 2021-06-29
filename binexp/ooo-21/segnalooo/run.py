import os

for i in range(0x100):
  if i != 241:
    os.system("./a.out %d" % i)
