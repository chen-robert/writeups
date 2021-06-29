#!/usr/bin/env python3

from pwn import *
import random
import os

num_sent = 0
while True:
    num_sent = 0
    print("Restarting...")
    p = process('./dual')

    last_text_len = None

    fd = open(b'poc', 'wb')
    def sendline(payload):
        global num_sent
        fd.write(payload + b'\n')
        p.sendline(payload)
        num_sent += 1

#context.log_level = 'debug'
    with log.progress('Fuzzing progress') as s:
        while True:
            if num_sent >= 15000:
                p.close()
                break
            elif num_sent % 1000 == 0:
                s.status('Tried %d/150000 operations' % num_sent)
            
            op = p.recvuntil(b'>\n', drop=True).rsplit(b'\n', 1)[-1]
            #print('Current operation:', op)
            if op[-2:] == b'op':
                sendline(str(random.choice(range(1,7+1))).encode())
            elif op in [b'pred_id', b'succ_id', b'node_id']:
                sendline(random.choice(['1','2','3', str(random.randint(1, 10000))]).encode())
            elif op in [b'text_len', b'bin_len']:
                last_text_len = random.randint(2, 200)
                sendline(str(last_text_len).encode())
            elif op in [b'bin', b'text']:
                sendline(b"A" * (last_text_len-1))
            else:
                continue
                #p.interactive()
                #raise ValueError('Unknown op:' + str(op))

    
