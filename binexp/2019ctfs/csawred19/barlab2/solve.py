from pwn import *

#p = process("./output", aslr=False)
p = remote("rev.chal.csaw.io", 1002)

target1 = [0] * 28
target1[0] = 0x6a;
target1[1] = 0x35;
target1[2] = 0x6a;
target1[3] = 0x6f;
target1[4] = 0x75;
target1[5] = 0x75;
target1[6] = 0x69;
target1[7] = 0x34;
target1[8] = 100;
target1[9] = 0x41;
target1[10] = 0x75;
target1[11] = 0x7a;
target1[12] = 0x35;
target1[13] = 0x6d;
target1[14] = 0x6d;
target1[15] = 0x74;
target1[16] = 0x62;
target1[17] = 0x78;
target1[18] = 0x7a;
target1[19] = 0x34;
target1[20] = 0x74;
target1[21] = 0x75;
target1[22] = 0x34;
target1[23] = 0x73;
target1[24] = 0x65;
target1[25] = 0x41;
target1[26] = 0x7a;
target1[27] = 0xb;

ret1 = ""
for i in range(0x1b):
  ret1 += chr(target1[i] - 1)
p.sendline(ret1)

target2 = [0] * 36
target2[0] = 99;
target2[1] = 0x70;
target2[2] = 0x68;
target2[3] = 99;
target2[4] = 0x81;
target2[5] = 0x73;
target2[6] = 0x6e;
target2[7] = 0x6b;
target2[8] = 0x50;
target2[9] = 0x56;
target2[10] = 0x57;
target2[11] = 0x68;
target2[12] = 0x82;
target2[13] = 0x76;
target2[14] = 0x52;
target2[15] = 0x53;
target2[16] = 0x4e;
target2[17] = 0x53;
target2[18] = 0x72;
target2[19] = 0x51;
target2[20] = 0x53;
target2[21] = 0x54;
target2[22] = 0x54;
target2[23] = 0x53;
target2[24] = 0x53;
target2[25] = 0x71;
target2[26] = 0x6b;
target2[27] = 0x82;
target2[28] = 0x56;
target2[29] = 0x81;
target2[30] = 0x73;
target2[31] = 0x78;
target2[32] = 0x5b;
target2[33] = 99;
target2[34] = 0x41;
target2[35] = 0x2a;

ret2 = ""
for i in range(0x22):
  nxt = target2[i] - 0x20
  if 0x1f < nxt and nxt < 0x5b:
#    print(i)
#    assert nxt > 0x1f + 3
    nxt -= 3
  ret2 += chr(nxt)
ret2 += chr(100 + (0x41 - 0x37) * 2) + chr(0xa)

print(ret1)
print(ret2)

p.sendline(ret2)

p.interactive()
