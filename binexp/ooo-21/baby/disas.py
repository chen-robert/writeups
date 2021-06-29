import struct
import string

opcode = [hex(i) for i in range(256)]
opcode[0x8] = 'hlt'
opcode[0xd] = 'sub'
opcode[0xf] = 'lt'
opcode[0x10] = 'eq'
opcode[0x11] = 'add'
opcode[0x12] = 'gt'
opcode[0x16] = 'mul'
opcode[0x17] = 'xor'
opcode[0x19] = 'or'
opcode[0x1a] = 'shl'
opcode[0x1b] = 'shr'
opcode[0x1c] = 'neq'
opcode[0x1f] = 'geq'
opcode[0x20] = 'leq'
opcode[0x26] = 'mod'

def pp(n):
    s = hex(n)[2:]
    s = bytes.fromhex(['', '0'][len(s)%2] + s).decode('latin1')
    if len(s) > 3 and not(set(s) - set(string.printable)):
        return repr(s[::-1])
    return hex(n)

f = open("os", "rb").read()[14644:]
for i in range(0, len(f), 40):
    u = struct.unpack('<IIIIQQII', f[i:i+40])
    instr = {'op': opcode[u[0]], '4': pp(u[1]), '8': pp(u[2]), '12': pp(u[3]), 'lit1': pp(u[5]), 'lit2': pp(u[4]), 'dest1': pp(u[6]), 'dest2': pp(u[7])}
    assert u[7] == 0
    print(", ".join(f"{k}= {instr[k]}" for k in instr))

exit()

f = open("p", "rb").read()+b"\x00"
assert(len(f)/40 == 79)
for i in range(0, len(f), 40):
    instr = struct.unpack('<IHHQQQII', f[i:i+40])
    opcode = instr[4]
    print(instr)
