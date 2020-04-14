from pwn import *
from ctypes import *

from time import time as t

cdll.LoadLibrary('libc.so.6')
libc = CDLL('libc.so.6')

time = lambda : int(t())

#p = process('./troll')
p = remote("ctf.umbccd.io", 5600)

libc.srand(time())

for i in range(3):
	A = libc.rand() ^ libc.rand()
	print(A)

p.interactive()
