// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.security.InvalidParameterException;
import java.io.Serializable;

public class CPU implements Serializable
{
    private static final long serialVersionUID = 3042928203064585497L;
    MMU mem;
    RegisterFile regs;
    InterruptHandler interruptHandler;
    private int clockCycleDelta;
    public boolean interrupted;
    public int pendingInterrupt;
    private int clockCycles;
    public static final int ZFLAG = 7;
    public static final int NFLAG = 6;
    public static final int HFLAG = 5;
    public static final int CFLAG = 4;
    public static final int NOJUMP = -1;
    public static final int RELJUMP = 0;
    public static final int ABSJUMP = 1;
    boolean halted;
    static Operation[] operations;
    static Operation[] cbOperations;
    
    public CPU(final MMU mem) {
        this.regs = new RegisterFile();
        this.interruptHandler = new InterruptHandler(this);
        this.interrupted = false;
        this.pendingInterrupt = 0;
        this.clockCycles = 0;
        this.halted = false;
        CPU.operations[0] = new Operation("NOP", CPU::NOP, 1, "- - - -", 4);
        CPU.operations[1] = new Operation("LD BC,d16", cpu -> cpu.LD(cpu.regs.BC, cpu.d16()), 3, "- - - -", 12);
        CPU.operations[2] = new Operation("LD (BC),A", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.BC), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[3] = new Operation("INC BC", cpu -> cpu.INC(cpu.regs.BC), 1, "- - - -", 8);
        CPU.operations[4] = new Operation("INC B", cpu -> cpu.INC(cpu.regs.B), 1, "Z 0 H -", 4);
        CPU.operations[5] = new Operation("DEC B", cpu -> cpu.DEC(cpu.regs.B), 1, "Z 1 H -", 4);
        CPU.operations[6] = new Operation("LD B,d8", cpu -> cpu.LD(cpu.regs.B, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[7] = new Operation("RLCA", CPU::RLCA, 1, "0 0 0 C", 4);
        CPU.operations[8] = new Operation("LD (a16),SP", cpu -> cpu.LD(cpu.mem.a16Location(cpu.regs.PC), cpu.regs.SP), 3, "- - - -", 20);
        CPU.operations[9] = new Operation("ADD HL,BC", cpu -> cpu.ADD(cpu.regs.HL, cpu.regs.BC), 1, "- 0 H C", 8);
        CPU.operations[10] = new Operation("LD A,(BC)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.registerLocation(cpu.regs.BC)), 1, "- - - -", 8);
        CPU.operations[11] = new Operation("DEC BC", cpu -> cpu.DEC(cpu.regs.BC), 1, "- - - -", 8);
        CPU.operations[12] = new Operation("INC C", cpu -> cpu.INC(cpu.regs.C), 1, "Z 0 H -", 4);
        CPU.operations[13] = new Operation("DEC C", cpu -> cpu.DEC(cpu.regs.C), 1, "Z 1 H -", 4);
        CPU.operations[14] = new Operation("LD C,d8", cpu -> cpu.LD(cpu.regs.C, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[15] = new Operation("RRCA", CPU::RRCA, 1, "0 0 0 C", 4);
        CPU.operations[16] = new Operation("STOP", CPU::STOP, 2, "- - - -", 4);
        CPU.operations[17] = new Operation("LD DE,d16", cpu -> cpu.LD(cpu.regs.DE, cpu.d16()), 3, "- - - -", 12);
        CPU.operations[18] = new Operation("LD (DE),A", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.DE), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[19] = new Operation("INC DE", cpu -> cpu.INC(cpu.regs.DE), 1, "- - - -", 8);
        CPU.operations[20] = new Operation("INC D", cpu -> cpu.INC(cpu.regs.D), 1, "Z 0 H -", 4);
        CPU.operations[21] = new Operation("DEC D", cpu -> cpu.DEC(cpu.regs.D), 1, "Z 1 H -", 4);
        CPU.operations[22] = new Operation("LD D,d8", cpu -> cpu.LD(cpu.regs.D, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[23] = new Operation("RLA", CPU::RLA, 1, "0 0 0 C", 4);
        CPU.operations[24] = new Jump("JR r8", cpu -> cpu.JR(cpu.d8()), 2, "- - - -", 12, 12);
        CPU.operations[25] = new Operation("ADD HL,DE", cpu -> cpu.ADD(cpu.regs.HL, cpu.regs.DE), 1, "- 0 H C", 8);
        CPU.operations[26] = new Operation("LD A,(DE)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.registerLocation(cpu.regs.DE)), 1, "- - - -", 8);
        CPU.operations[27] = new Operation("DEC DE", cpu -> cpu.DEC(cpu.regs.DE), 1, "- - - -", 8);
        CPU.operations[28] = new Operation("INC E", cpu -> cpu.INC(cpu.regs.E), 1, "Z 0 H -", 4);
        CPU.operations[29] = new Operation("DEC E", cpu -> cpu.DEC(cpu.regs.E), 1, "Z 1 H -", 4);
        CPU.operations[30] = new Operation("LD E,d8", cpu -> cpu.LD(cpu.regs.E, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[31] = new Operation("RRA", CPU::RRA, 1, "0 0 0 C", 4);
        CPU.operations[32] = new Jump("JR NZ,r8", cpu -> cpu.JR(Condition.NZ, cpu.d8()), 2, "- - - -", 12, 8);
        CPU.operations[33] = new Operation("LD HL,d16", cpu -> cpu.LD(cpu.regs.HL, cpu.d16()), 3, "- - - -", 12);
        CPU.operations[34] = new Operation("LD (HL+),A", cpu -> cpu.LD(cpu.mem.registerLocation(this.selfIncrement(cpu.regs.HL)), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[35] = new Operation("INC HL", cpu -> cpu.INC(cpu.regs.HL), 1, "- - - -", 8);
        CPU.operations[36] = new Operation("INC H", cpu -> cpu.INC(cpu.regs.H), 1, "Z 0 H -", 4);
        CPU.operations[37] = new Operation("DEC H", cpu -> cpu.DEC(cpu.regs.H), 1, "Z 1 H -", 4);
        CPU.operations[38] = new Operation("LD H,d8", cpu -> cpu.LD(cpu.regs.H, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[39] = new Operation("DAA", CPU::DAA, 1, "Z - 0 C", 4);
        CPU.operations[40] = new Jump("JR Z,r8", cpu -> cpu.JR(Condition.Z, cpu.d8()), 2, "- - - -", 12, 8);
        CPU.operations[41] = new Operation("ADD HL,HL", cpu -> cpu.ADD(cpu.regs.HL, cpu.regs.HL), 1, "- 0 H C", 8);
        CPU.operations[42] = new Operation("LD A,(HL+)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.registerLocation(this.selfIncrement(cpu.regs.HL))), 1, "- - - -", 8);
        CPU.operations[43] = new Operation("DEC HL", cpu -> cpu.DEC(cpu.regs.HL), 1, "- - - -", 8);
        CPU.operations[44] = new Operation("INC L", cpu -> cpu.INC(cpu.regs.L), 1, "Z 0 H -", 4);
        CPU.operations[45] = new Operation("DEC L", cpu -> cpu.DEC(cpu.regs.L), 1, "Z 1 H -", 4);
        CPU.operations[46] = new Operation("LD L,d8", cpu -> cpu.LD(cpu.regs.L, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[47] = new Operation("CPL", CPU::CPL, 1, "- 1 1 -", 4);
        CPU.operations[48] = new Jump("JR NC,r8", cpu -> cpu.JR(Condition.NC, cpu.d8()), 2, "- - - -", 12, 8);
        CPU.operations[49] = new Operation("LD SP,d16", cpu -> cpu.LD(cpu.regs.SP, cpu.d16()), 3, "- - - -", 12);
        CPU.operations[50] = new Operation("LD (HL-),A", cpu -> cpu.LD(cpu.mem.registerLocation(this.selfDecrement(cpu.regs.HL)), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[51] = new Operation("INC SP", cpu -> cpu.INC(cpu.regs.SP), 1, "- - - -", 8);
        CPU.operations[52] = new Operation("INC (HL)", cpu -> cpu.INC(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 H -", 12);
        CPU.operations[53] = new Operation("DEC (HL)", cpu -> cpu.DEC(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 1 H -", 12);
        CPU.operations[54] = new Operation("LD (HL),d8", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.d8()), 2, "- - - -", 12);
        CPU.operations[55] = new Operation("SCF", CPU::SCF, 1, "- 0 0 1", 4);
        CPU.operations[56] = new Jump("JR C(cond),r8", cpu -> cpu.JR(Condition.C, cpu.d8()), 2, "- - - -", 12, 8);
        CPU.operations[57] = new Operation("ADD HL,SP", cpu -> cpu.ADD(cpu.regs.HL, cpu.regs.SP), 1, "- 0 H C", 8);
        CPU.operations[58] = new Operation("LD A,(HL-)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.registerLocation(this.selfDecrement(cpu.regs.HL))), 1, "- - - -", 8);
        CPU.operations[59] = new Operation("DEC SP", cpu -> cpu.DEC(cpu.regs.SP), 1, "- - - -", 8);
        CPU.operations[60] = new Operation("INC A", cpu -> cpu.INC(cpu.regs.A), 1, "Z 0 H -", 4);
        CPU.operations[61] = new Operation("DEC A", cpu -> cpu.DEC(cpu.regs.A), 1, "Z 1 H -", 4);
        CPU.operations[62] = new Operation("LD A,d8", cpu -> cpu.LD(cpu.regs.A, cpu.d8()), 2, "- - - -", 8);
        CPU.operations[63] = new Operation("CCF", CPU::CCF, 1, "- 0 0 C", 4);
        CPU.operations[64] = new Operation("LD B,B", cpu -> cpu.LD(cpu.regs.B, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[65] = new Operation("LD B,C", cpu -> cpu.LD(cpu.regs.B, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[66] = new Operation("LD B,D", cpu -> cpu.LD(cpu.regs.B, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[67] = new Operation("LD B,E", cpu -> cpu.LD(cpu.regs.B, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[68] = new Operation("LD B,H", cpu -> cpu.LD(cpu.regs.B, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[69] = new Operation("LD B,L", cpu -> cpu.LD(cpu.regs.B, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[70] = new Operation("LD B,(HL)", cpu -> cpu.LD(cpu.regs.B, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[71] = new Operation("LD B,A", cpu -> cpu.LD(cpu.regs.B, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[72] = new Operation("LD C,B", cpu -> cpu.LD(cpu.regs.C, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[73] = new Operation("LD C,C", cpu -> cpu.LD(cpu.regs.C, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[74] = new Operation("LD C,D", cpu -> cpu.LD(cpu.regs.C, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[75] = new Operation("LD C,E", cpu -> cpu.LD(cpu.regs.C, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[76] = new Operation("LD C,H", cpu -> cpu.LD(cpu.regs.C, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[77] = new Operation("LD C,L", cpu -> cpu.LD(cpu.regs.C, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[78] = new Operation("LD C,(HL)", cpu -> cpu.LD(cpu.regs.C, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[79] = new Operation("LD C,A", cpu -> cpu.LD(cpu.regs.C, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[80] = new Operation("LD D,B", cpu -> cpu.LD(cpu.regs.D, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[81] = new Operation("LD D,C", cpu -> cpu.LD(cpu.regs.D, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[82] = new Operation("LD D,D", cpu -> cpu.LD(cpu.regs.D, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[83] = new Operation("LD D,E", cpu -> cpu.LD(cpu.regs.D, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[84] = new Operation("LD D,H", cpu -> cpu.LD(cpu.regs.D, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[85] = new Operation("LD D,L", cpu -> cpu.LD(cpu.regs.D, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[86] = new Operation("LD D,(HL)", cpu -> cpu.LD(cpu.regs.D, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[87] = new Operation("LD D,A", cpu -> cpu.LD(cpu.regs.D, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[88] = new Operation("LD E,B", cpu -> cpu.LD(cpu.regs.E, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[89] = new Operation("LD E,C", cpu -> cpu.LD(cpu.regs.E, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[90] = new Operation("LD E,D", cpu -> cpu.LD(cpu.regs.E, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[91] = new Operation("LD E,E", cpu -> cpu.LD(cpu.regs.E, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[92] = new Operation("LD E,H", cpu -> cpu.LD(cpu.regs.E, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[93] = new Operation("LD E,L", cpu -> cpu.LD(cpu.regs.E, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[94] = new Operation("LD E,(HL)", cpu -> cpu.LD(cpu.regs.E, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[95] = new Operation("LD E,A", cpu -> cpu.LD(cpu.regs.E, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[96] = new Operation("LD H,B", cpu -> cpu.LD(cpu.regs.H, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[97] = new Operation("LD H,C", cpu -> cpu.LD(cpu.regs.H, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[98] = new Operation("LD H,D", cpu -> cpu.LD(cpu.regs.H, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[99] = new Operation("LD H,E", cpu -> cpu.LD(cpu.regs.H, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[100] = new Operation("LD H,H", cpu -> cpu.LD(cpu.regs.H, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[101] = new Operation("LD H,L", cpu -> cpu.LD(cpu.regs.H, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[102] = new Operation("LD H,(HL)", cpu -> cpu.LD(cpu.regs.H, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[103] = new Operation("LD H,A", cpu -> cpu.LD(cpu.regs.H, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[104] = new Operation("LD L,B", cpu -> cpu.LD(cpu.regs.L, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[105] = new Operation("LD L,C", cpu -> cpu.LD(cpu.regs.L, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[106] = new Operation("LD L,D", cpu -> cpu.LD(cpu.regs.L, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[107] = new Operation("LD L,E", cpu -> cpu.LD(cpu.regs.L, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[108] = new Operation("LD L,H", cpu -> cpu.LD(cpu.regs.L, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[109] = new Operation("LD L,L", cpu -> cpu.LD(cpu.regs.L, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[110] = new Operation("LD L,(HL)", cpu -> cpu.LD(cpu.regs.L, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[111] = new Operation("LD L,A", cpu -> cpu.LD(cpu.regs.L, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[112] = new Operation("LD (HL),B", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.B), 1, "- - - -", 8);
        CPU.operations[113] = new Operation("LD (HL),C", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.C), 1, "- - - -", 8);
        CPU.operations[114] = new Operation("LD (HL),D", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.D), 1, "- - - -", 8);
        CPU.operations[115] = new Operation("LD (HL),E", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.E), 1, "- - - -", 8);
        CPU.operations[116] = new Operation("LD (HL),H", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.H), 1, "- - - -", 8);
        CPU.operations[117] = new Operation("LD (HL),L", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.L), 1, "- - - -", 8);
        CPU.operations[118] = new Operation("HALT", CPU::HALT, 1, "- - - -", 4);
        CPU.operations[119] = new Operation("LD (HL),A", cpu -> cpu.LD(cpu.mem.registerLocation(cpu.regs.HL), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[120] = new Operation("LD A,B", cpu -> cpu.LD(cpu.regs.A, cpu.regs.B), 1, "- - - -", 4);
        CPU.operations[121] = new Operation("LD A,C", cpu -> cpu.LD(cpu.regs.A, cpu.regs.C), 1, "- - - -", 4);
        CPU.operations[122] = new Operation("LD A,D", cpu -> cpu.LD(cpu.regs.A, cpu.regs.D), 1, "- - - -", 4);
        CPU.operations[123] = new Operation("LD A,E", cpu -> cpu.LD(cpu.regs.A, cpu.regs.E), 1, "- - - -", 4);
        CPU.operations[124] = new Operation("LD A,H", cpu -> cpu.LD(cpu.regs.A, cpu.regs.H), 1, "- - - -", 4);
        CPU.operations[125] = new Operation("LD A,L", cpu -> cpu.LD(cpu.regs.A, cpu.regs.L), 1, "- - - -", 4);
        CPU.operations[126] = new Operation("LD A,(HL)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.registerLocation(cpu.regs.HL)), 1, "- - - -", 8);
        CPU.operations[127] = new Operation("LD A,A", cpu -> cpu.LD(cpu.regs.A, cpu.regs.A), 1, "- - - -", 4);
        CPU.operations[128] = new Operation("ADD A,B", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.B), 1, "Z 0 H C", 4);
        CPU.operations[129] = new Operation("ADD A,C", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.C), 1, "Z 0 H C", 4);
        CPU.operations[130] = new Operation("ADD A,D", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.D), 1, "Z 0 H C", 4);
        CPU.operations[131] = new Operation("ADD A,E", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.E), 1, "Z 0 H C", 4);
        CPU.operations[132] = new Operation("ADD A,H", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.H), 1, "Z 0 H C", 4);
        CPU.operations[133] = new Operation("ADD A,L", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.L), 1, "Z 0 H C", 4);
        CPU.operations[134] = new Operation("ADD A,(HL)", cpu -> cpu.ADD(cpu.regs.A, cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 H C", 8);
        CPU.operations[135] = new Operation("ADD A,A", cpu -> cpu.ADD(cpu.regs.A, cpu.regs.A), 1, "Z 0 H C", 4);
        CPU.operations[136] = new Operation("ADC A,B", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.B), 1, "Z 0 H C", 4);
        CPU.operations[137] = new Operation("ADC A,C", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.C), 1, "Z 0 H C", 4);
        CPU.operations[138] = new Operation("ADC A,D", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.D), 1, "Z 0 H C", 4);
        CPU.operations[139] = new Operation("ADC A,E", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.E), 1, "Z 0 H C", 4);
        CPU.operations[140] = new Operation("ADC A,H", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.H), 1, "Z 0 H C", 4);
        CPU.operations[141] = new Operation("ADC A,L", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.L), 1, "Z 0 H C", 4);
        CPU.operations[142] = new Operation("ADC A,(HL)", cpu -> cpu.ADC(cpu.regs.A, cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 H C", 8);
        CPU.operations[143] = new Operation("ADC A,A", cpu -> cpu.ADC(cpu.regs.A, cpu.regs.A), 1, "Z 0 H C", 4);
        CPU.operations[144] = new Operation("SUB B", cpu -> cpu.SUB(cpu.regs.B), 1, "Z 1 H C", 4);
        CPU.operations[145] = new Operation("SUB C", cpu -> cpu.SUB(cpu.regs.C), 1, "Z 1 H C", 4);
        CPU.operations[146] = new Operation("SUB D", cpu -> cpu.SUB(cpu.regs.D), 1, "Z 1 H C", 4);
        CPU.operations[147] = new Operation("SUB E", cpu -> cpu.SUB(cpu.regs.E), 1, "Z 1 H C", 4);
        CPU.operations[148] = new Operation("SUB H", cpu -> cpu.SUB(cpu.regs.H), 1, "Z 1 H C", 4);
        CPU.operations[149] = new Operation("SUB L", cpu -> cpu.SUB(cpu.regs.L), 1, "Z 1 H C", 4);
        CPU.operations[150] = new Operation("SUB (HL)", cpu -> cpu.SUB(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 1 H C", 8);
        CPU.operations[151] = new Operation("SUB A", cpu -> cpu.SUB(cpu.regs.A), 1, "Z 1 H C", 4);
        CPU.operations[152] = new Operation("SBC B", cpu -> cpu.SBC(cpu.regs.B), 1, "Z 1 H C", 4);
        CPU.operations[153] = new Operation("SBC C", cpu -> cpu.SBC(cpu.regs.C), 1, "Z 1 H C", 4);
        CPU.operations[154] = new Operation("SBC D", cpu -> cpu.SBC(cpu.regs.D), 1, "Z 1 H C", 4);
        CPU.operations[155] = new Operation("SBC E", cpu -> cpu.SBC(cpu.regs.E), 1, "Z 1 H C", 4);
        CPU.operations[156] = new Operation("SBC H", cpu -> cpu.SBC(cpu.regs.H), 1, "Z 1 H C", 4);
        CPU.operations[157] = new Operation("SBC L", cpu -> cpu.SBC(cpu.regs.L), 1, "Z 1 H C", 4);
        CPU.operations[158] = new Operation("SBC (HL)", cpu -> cpu.SBC(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 1 H C", 8);
        CPU.operations[159] = new Operation("SBC A", cpu -> cpu.SBC(cpu.regs.A), 1, "Z 1 H C", 4);
        CPU.operations[160] = new Operation("AND B", cpu -> cpu.AND(cpu.regs.B), 1, "Z 0 1 0", 4);
        CPU.operations[161] = new Operation("AND C", cpu -> cpu.AND(cpu.regs.C), 1, "Z 0 1 0", 4);
        CPU.operations[162] = new Operation("AND D", cpu -> cpu.AND(cpu.regs.D), 1, "Z 0 1 0", 4);
        CPU.operations[163] = new Operation("AND E", cpu -> cpu.AND(cpu.regs.E), 1, "Z 0 1 0", 4);
        CPU.operations[164] = new Operation("AND H", cpu -> cpu.AND(cpu.regs.H), 1, "Z 0 1 0", 4);
        CPU.operations[165] = new Operation("AND L", cpu -> cpu.AND(cpu.regs.L), 1, "Z 0 1 0", 4);
        CPU.operations[166] = new Operation("AND (HL)", cpu -> cpu.AND(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 1 0", 8);
        CPU.operations[167] = new Operation("AND A", cpu -> cpu.AND(cpu.regs.A), 1, "Z 0 1 0", 4);
        CPU.operations[168] = new Operation("XOR B", cpu -> cpu.XOR(cpu.regs.B), 1, "Z 0 0 0", 4);
        CPU.operations[169] = new Operation("XOR C", cpu -> cpu.XOR(cpu.regs.C), 1, "Z 0 0 0", 4);
        CPU.operations[170] = new Operation("XOR D", cpu -> cpu.XOR(cpu.regs.D), 1, "Z 0 0 0", 4);
        CPU.operations[171] = new Operation("XOR E", cpu -> cpu.XOR(cpu.regs.E), 1, "Z 0 0 0", 4);
        CPU.operations[172] = new Operation("XOR H", cpu -> cpu.XOR(cpu.regs.H), 1, "Z 0 0 0", 4);
        CPU.operations[173] = new Operation("XOR L", cpu -> cpu.XOR(cpu.regs.L), 1, "Z 0 0 0", 4);
        CPU.operations[174] = new Operation("XOR (HL)", cpu -> cpu.XOR(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 0 0", 8);
        CPU.operations[175] = new Operation("XOR A", cpu -> cpu.XOR(cpu.regs.A), 1, "Z 0 0 0", 4);
        CPU.operations[176] = new Operation("OR B", cpu -> cpu.OR(cpu.regs.B), 1, "Z 0 0 0", 4);
        CPU.operations[177] = new Operation("OR C", cpu -> cpu.OR(cpu.regs.C), 1, "Z 0 0 0", 4);
        CPU.operations[178] = new Operation("OR D", cpu -> cpu.OR(cpu.regs.D), 1, "Z 0 0 0", 4);
        CPU.operations[179] = new Operation("OR E", cpu -> cpu.OR(cpu.regs.E), 1, "Z 0 0 0", 4);
        CPU.operations[180] = new Operation("OR H", cpu -> cpu.OR(cpu.regs.H), 1, "Z 0 0 0", 4);
        CPU.operations[181] = new Operation("OR L", cpu -> cpu.OR(cpu.regs.L), 1, "Z 0 0 0", 4);
        CPU.operations[182] = new Operation("OR (HL)", cpu -> cpu.OR(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 0 0 0", 8);
        CPU.operations[183] = new Operation("OR A", cpu -> cpu.OR(cpu.regs.A), 1, "Z 0 0 0", 4);
        CPU.operations[184] = new Operation("CP B", cpu -> cpu.CP(cpu.regs.B), 1, "Z 1 H C", 4);
        CPU.operations[185] = new Operation("CP C", cpu -> cpu.CP(cpu.regs.C), 1, "Z 1 H C", 4);
        CPU.operations[186] = new Operation("CP D", cpu -> cpu.CP(cpu.regs.D), 1, "Z 1 H C", 4);
        CPU.operations[187] = new Operation("CP E", cpu -> cpu.CP(cpu.regs.E), 1, "Z 1 H C", 4);
        CPU.operations[188] = new Operation("CP H", cpu -> cpu.CP(cpu.regs.H), 1, "Z 1 H C", 4);
        CPU.operations[189] = new Operation("CP L", cpu -> cpu.CP(cpu.regs.L), 1, "Z 1 H C", 4);
        CPU.operations[190] = new Operation("CP (HL)", cpu -> cpu.CP(cpu.mem.registerLocation(cpu.regs.HL)), 1, "Z 1 H C", 8);
        CPU.operations[191] = new Operation("CP A", cpu -> cpu.CP(cpu.regs.A), 1, "Z 1 H C", 4);
        CPU.operations[192] = new Jump("RET NZ", cpu -> cpu.RET(Condition.NZ), 1, "- - - -", 20, 8);
        CPU.operations[193] = new Operation("POP BC", cpu -> cpu.POP(cpu.regs.BC), 1, "- - - -", 12);
        CPU.operations[194] = new Jump("JP NZ,a16", cpu -> cpu.JP(Condition.NZ, cpu.a16()), 3, "- - - -", 16, 12);
        CPU.operations[195] = new Jump("JP a16", cpu -> cpu.JP(cpu.a16()), 3, "- - - -", 16, 16);
        CPU.operations[196] = new Jump("CALL NZ,a16", cpu -> cpu.CALL(Condition.NZ, cpu.a16()), 3, "- - - -", 24, 12);
        CPU.operations[197] = new Operation("PUSH BC", cpu -> cpu.PUSH(cpu.regs.BC), 1, "- - - -", 16);
        CPU.operations[198] = new Operation("ADD A,d8", cpu -> cpu.ADD(cpu.regs.A, cpu.d8()), 2, "Z 0 H C", 8);
        CPU.operations[199] = new Jump("RST 00H", cpu -> cpu.RST(0), 1, "- - - -", 16, 16);
        CPU.operations[200] = new Jump("RET Z", cpu -> cpu.RET(Condition.Z), 1, "- - - -", 20, 8);
        CPU.operations[201] = new Jump("RET", CPU::RET, 1, "- - - -", 16, 16);
        CPU.operations[202] = new Jump("JP Z,a16", cpu -> cpu.JP(Condition.Z, cpu.a16()), 3, "- - - -", 16, 12);
        CPU.operations[203] = new CB();
        CPU.operations[204] = new Jump("CALL Z,a16", cpu -> cpu.CALL(Condition.Z, cpu.a16()), 3, "- - - -", 24, 12);
        CPU.operations[205] = new Jump("CALL a16", cpu -> cpu.CALL(cpu.a16()), 3, "- - - -", 24, 24);
        CPU.operations[206] = new Operation("ADC A,d8", cpu -> cpu.ADC(cpu.regs.A, cpu.d8()), 2, "Z 0 H C", 8);
        CPU.operations[207] = new Jump("RST 08H", cpu -> cpu.RST(8), 1, "- - - -", 16, 16);
        CPU.operations[208] = new Jump("RET NC", cpu -> cpu.RET(Condition.NC), 1, "- - - -", 20, 8);
        CPU.operations[209] = new Operation("POP DE", cpu -> cpu.POP(cpu.regs.DE), 1, "- - - -", 12);
        CPU.operations[210] = new Jump("JP NC,a16", cpu -> cpu.JP(Condition.NC, cpu.a16()), 3, "- - - -", 16, 12);
        CPU.operations[211] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[212] = new Jump("CALL NC,a16", cpu -> cpu.CALL(Condition.NC, cpu.a16()), 3, "- - - -", 24, 12);
        CPU.operations[213] = new Operation("PUSH DE", cpu -> cpu.PUSH(cpu.regs.DE), 1, "- - - -", 16);
        CPU.operations[214] = new Operation("SUB d8", cpu -> cpu.SUB(cpu.d8()), 2, "Z 1 H C", 8);
        CPU.operations[215] = new Jump("RST 10H", cpu -> cpu.RST(16), 1, "- - - -", 16, 16);
        CPU.operations[216] = new Jump("RET C(cond)", cpu -> cpu.RET(Condition.C), 1, "- - - -", 20, 8);
        CPU.operations[217] = new Jump("RETI", CPU::RETI, 1, "- - - -", 16, 16);
        CPU.operations[218] = new Jump("JP C(cond),a16", cpu -> cpu.JP(Condition.C, cpu.a16()), 3, "- - - -", 16, 12);
        CPU.operations[219] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[220] = new Jump("CALL C(cond),a16", cpu -> cpu.CALL(Condition.C, cpu.a16()), 3, "- - - -", 24, 12);
        CPU.operations[221] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[222] = new Operation("SBC d8", cpu -> cpu.SBC(cpu.d8()), 2, "Z 1 H C", 8);
        CPU.operations[223] = new Jump("RST 18H", cpu -> cpu.RST(24), 1, "- - - -", 16, 16);
        CPU.operations[224] = new Operation("LD (a8),A", cpu -> cpu.LD(cpu.mem.a8Location(cpu.regs.PC), cpu.regs.A), 2, "- - - -", 12);
        CPU.operations[225] = new Operation("POP HL", cpu -> cpu.POP(cpu.regs.HL), 1, "- - - -", 12);
        CPU.operations[226] = new Operation("LD (C),A", cpu -> cpu.LD(cpu.mem.shortRegisterLocation(cpu.regs.C), cpu.regs.A), 1, "- - - -", 8);
        CPU.operations[227] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[228] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[229] = new Operation("PUSH HL", cpu -> cpu.PUSH(cpu.regs.HL), 1, "- - - -", 16);
        CPU.operations[230] = new Operation("AND d8", cpu -> cpu.AND(cpu.d8()), 2, "Z 0 1 0", 8);
        CPU.operations[231] = new Jump("RST 20H", cpu -> cpu.RST(32), 1, "- - - -", 16, 16);
        CPU.operations[232] = new Operation("ADD SP,r8", cpu -> cpu.ADD(cpu.regs.SP, cpu.r8()), 2, "0 0 H C", 16);
        CPU.operations[233] = new Jump("JP HL", cpu -> cpu.JP(cpu.regs.HL), 1, "- - - -", 4, 4);
        CPU.operations[234] = new Operation("LD (a16),A", cpu -> cpu.LD(cpu.mem.a16Location(cpu.regs.PC), cpu.regs.A), 3, "- - - -", 16);
        CPU.operations[235] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[236] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[237] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[238] = new Operation("XOR d8", cpu -> cpu.XOR(cpu.d8()), 2, "Z 0 0 0", 8);
        CPU.operations[239] = new Jump("RST 28H", cpu -> cpu.RST(40), 1, "- - - -", 16, 16);
        CPU.operations[240] = new Operation("LD A,(a8)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.a8Location(cpu.regs.PC)), 2, "- - - -", 12);
        CPU.operations[241] = new Operation("POP AF", cpu -> cpu.POP(cpu.regs.AF), 1, "Z N H C", 12);
        CPU.operations[242] = new Operation("LD A,(C)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.shortRegisterLocation(cpu.regs.C)), 1, "- - - -", 8);
        CPU.operations[243] = new Operation("DI", CPU::DI, 1, "- - - -", 4);
        CPU.operations[244] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[245] = new Operation("PUSH AF", cpu -> cpu.PUSH(cpu.regs.AF), 1, "- - - -", 16);
        CPU.operations[246] = new Operation("OR d8", cpu -> cpu.OR(cpu.d8()), 2, "Z 0 0 0", 8);
        CPU.operations[247] = new Jump("RST 30H", cpu -> cpu.RST(48), 1, "- - - -", 16, 16);
        CPU.operations[248] = new Operation("LD HL,SP+r8", cpu -> cpu.LD(cpu.regs.HL, cpu.SPr8()), 2, "0 0 H C", 12);
        CPU.operations[249] = new Operation("LD SP,HL", cpu -> cpu.LD(cpu.regs.SP, cpu.regs.HL), 1, "- - - -", 8);
        CPU.operations[250] = new Operation("LD A,(a16)", cpu -> cpu.LD(cpu.regs.A, cpu.mem.a16Location(cpu.regs.PC)), 3, "- - - -", 16);
        CPU.operations[251] = new Operation("EI", CPU::EI, 1, "- - - -", 4);
        CPU.operations[252] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[253] = new Operation("XXX", CPU::XXX, 0, "- - - -", 0);
        CPU.operations[254] = new Operation("CP d8", cpu -> cpu.CP(cpu.d8()), 2, "Z 1 H C", 8);
        CPU.operations[255] = new Jump("RST 38H", cpu -> cpu.RST(56), 1, "- - - -", 16, 16);
        CPU.cbOperations[0] = new Operation("RLC B", cpu -> cpu.RLC(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[1] = new Operation("RLC C", cpu -> cpu.RLC(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[2] = new Operation("RLC D", cpu -> cpu.RLC(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[3] = new Operation("RLC E", cpu -> cpu.RLC(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[4] = new Operation("RLC H", cpu -> cpu.RLC(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[5] = new Operation("RLC L", cpu -> cpu.RLC(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[6] = new Operation("RLC (HL)", cpu -> cpu.RLC(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[7] = new Operation("RLC A", cpu -> cpu.RLC(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[8] = new Operation("RRC B", cpu -> cpu.RRC(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[9] = new Operation("RRC C", cpu -> cpu.RRC(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[10] = new Operation("RRC D", cpu -> cpu.RRC(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[11] = new Operation("RRC E", cpu -> cpu.RRC(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[12] = new Operation("RRC H", cpu -> cpu.RRC(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[13] = new Operation("RRC L", cpu -> cpu.RRC(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[14] = new Operation("RRC (HL)", cpu -> cpu.RRC(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[15] = new Operation("RRC A", cpu -> cpu.RRC(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[16] = new Operation("RL B", cpu -> cpu.RL(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[17] = new Operation("RL C", cpu -> cpu.RL(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[18] = new Operation("RL D", cpu -> cpu.RL(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[19] = new Operation("RL E", cpu -> cpu.RL(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[20] = new Operation("RL H", cpu -> cpu.RL(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[21] = new Operation("RL L", cpu -> cpu.RL(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[22] = new Operation("RL (HL)", cpu -> cpu.RL(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[23] = new Operation("RL A", cpu -> cpu.RL(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[24] = new Operation("RR B", cpu -> cpu.RR(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[25] = new Operation("RR C", cpu -> cpu.RR(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[26] = new Operation("RR D", cpu -> cpu.RR(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[27] = new Operation("RR E", cpu -> cpu.RR(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[28] = new Operation("RR H", cpu -> cpu.RR(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[29] = new Operation("RR L", cpu -> cpu.RR(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[30] = new Operation("RR (HL)", cpu -> cpu.RR(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[31] = new Operation("RR A", cpu -> cpu.RR(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[32] = new Operation("SLA B", cpu -> cpu.SLA(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[33] = new Operation("SLA C", cpu -> cpu.SLA(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[34] = new Operation("SLA D", cpu -> cpu.SLA(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[35] = new Operation("SLA E", cpu -> cpu.SLA(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[36] = new Operation("SLA H", cpu -> cpu.SLA(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[37] = new Operation("SLA L", cpu -> cpu.SLA(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[38] = new Operation("SLA (HL)", cpu -> cpu.SLA(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[39] = new Operation("SLA A", cpu -> cpu.SLA(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[40] = new Operation("SRA B", cpu -> cpu.SRA(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[41] = new Operation("SRA C", cpu -> cpu.SRA(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[42] = new Operation("SRA D", cpu -> cpu.SRA(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[43] = new Operation("SRA E", cpu -> cpu.SRA(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[44] = new Operation("SRA H", cpu -> cpu.SRA(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[45] = new Operation("SRA L", cpu -> cpu.SRA(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[46] = new Operation("SRA (HL)", cpu -> cpu.SRA(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[47] = new Operation("SRA A", cpu -> cpu.SRA(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[48] = new Operation("SWAP B", cpu -> cpu.SWAP(cpu.regs.B), 2, "Z 0 0 0", 8);
        CPU.cbOperations[49] = new Operation("SWAP C", cpu -> cpu.SWAP(cpu.regs.C), 2, "Z 0 0 0", 8);
        CPU.cbOperations[50] = new Operation("SWAP D", cpu -> cpu.SWAP(cpu.regs.D), 2, "Z 0 0 0", 8);
        CPU.cbOperations[51] = new Operation("SWAP E", cpu -> cpu.SWAP(cpu.regs.E), 2, "Z 0 0 0", 8);
        CPU.cbOperations[52] = new Operation("SWAP H", cpu -> cpu.SWAP(cpu.regs.H), 2, "Z 0 0 0", 8);
        CPU.cbOperations[53] = new Operation("SWAP L", cpu -> cpu.SWAP(cpu.regs.L), 2, "Z 0 0 0", 8);
        CPU.cbOperations[54] = new Operation("SWAP (HL)", cpu -> cpu.SWAP(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 0", 16);
        CPU.cbOperations[55] = new Operation("SWAP A", cpu -> cpu.SWAP(cpu.regs.A), 2, "Z 0 0 0", 8);
        CPU.cbOperations[56] = new Operation("SRL B", cpu -> cpu.SRL(cpu.regs.B), 2, "Z 0 0 C", 8);
        CPU.cbOperations[57] = new Operation("SRL C", cpu -> cpu.SRL(cpu.regs.C), 2, "Z 0 0 C", 8);
        CPU.cbOperations[58] = new Operation("SRL D", cpu -> cpu.SRL(cpu.regs.D), 2, "Z 0 0 C", 8);
        CPU.cbOperations[59] = new Operation("SRL E", cpu -> cpu.SRL(cpu.regs.E), 2, "Z 0 0 C", 8);
        CPU.cbOperations[60] = new Operation("SRL H", cpu -> cpu.SRL(cpu.regs.H), 2, "Z 0 0 C", 8);
        CPU.cbOperations[61] = new Operation("SRL L", cpu -> cpu.SRL(cpu.regs.L), 2, "Z 0 0 C", 8);
        CPU.cbOperations[62] = new Operation("SRL (HL)", cpu -> cpu.SRL(cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 0 C", 16);
        CPU.cbOperations[63] = new Operation("SRL A", cpu -> cpu.SRL(cpu.regs.A), 2, "Z 0 0 C", 8);
        CPU.cbOperations[64] = new Operation("BIT 0,B", cpu -> cpu.BIT(0, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[65] = new Operation("BIT 0,C", cpu -> cpu.BIT(0, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[66] = new Operation("BIT 0,D", cpu -> cpu.BIT(0, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[67] = new Operation("BIT 0,E", cpu -> cpu.BIT(0, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[68] = new Operation("BIT 0,H", cpu -> cpu.BIT(0, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[69] = new Operation("BIT 0,L", cpu -> cpu.BIT(0, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[70] = new Operation("BIT 0,(HL)", cpu -> cpu.BIT(0, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[71] = new Operation("BIT 0,A", cpu -> cpu.BIT(0, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[72] = new Operation("BIT 1,B", cpu -> cpu.BIT(1, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[73] = new Operation("BIT 1,C", cpu -> cpu.BIT(1, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[74] = new Operation("BIT 1,D", cpu -> cpu.BIT(1, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[75] = new Operation("BIT 1,E", cpu -> cpu.BIT(1, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[76] = new Operation("BIT 1,H", cpu -> cpu.BIT(1, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[77] = new Operation("BIT 1,L", cpu -> cpu.BIT(1, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[78] = new Operation("BIT 1,(HL)", cpu -> cpu.BIT(1, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[79] = new Operation("BIT 1,A", cpu -> cpu.BIT(1, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[80] = new Operation("BIT 2,B", cpu -> cpu.BIT(2, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[81] = new Operation("BIT 2,C", cpu -> cpu.BIT(2, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[82] = new Operation("BIT 2,D", cpu -> cpu.BIT(2, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[83] = new Operation("BIT 2,E", cpu -> cpu.BIT(2, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[84] = new Operation("BIT 2,H", cpu -> cpu.BIT(2, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[85] = new Operation("BIT 2,L", cpu -> cpu.BIT(2, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[86] = new Operation("BIT 2,(HL)", cpu -> cpu.BIT(2, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[87] = new Operation("BIT 2,A", cpu -> cpu.BIT(2, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[88] = new Operation("BIT 3,B", cpu -> cpu.BIT(3, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[89] = new Operation("BIT 3,C", cpu -> cpu.BIT(3, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[90] = new Operation("BIT 3,D", cpu -> cpu.BIT(3, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[91] = new Operation("BIT 3,E", cpu -> cpu.BIT(3, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[92] = new Operation("BIT 3,H", cpu -> cpu.BIT(3, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[93] = new Operation("BIT 3,L", cpu -> cpu.BIT(3, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[94] = new Operation("BIT 3,(HL)", cpu -> cpu.BIT(3, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[95] = new Operation("BIT 3,A", cpu -> cpu.BIT(3, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[96] = new Operation("BIT 4,B", cpu -> cpu.BIT(4, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[97] = new Operation("BIT 4,C", cpu -> cpu.BIT(4, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[98] = new Operation("BIT 4,D", cpu -> cpu.BIT(4, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[99] = new Operation("BIT 4,E", cpu -> cpu.BIT(4, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[100] = new Operation("BIT 4,H", cpu -> cpu.BIT(4, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[101] = new Operation("BIT 4,L", cpu -> cpu.BIT(4, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[102] = new Operation("BIT 4,(HL)", cpu -> cpu.BIT(4, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[103] = new Operation("BIT 4,A", cpu -> cpu.BIT(4, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[104] = new Operation("BIT 5,B", cpu -> cpu.BIT(5, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[105] = new Operation("BIT 5,C", cpu -> cpu.BIT(5, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[106] = new Operation("BIT 5,D", cpu -> cpu.BIT(5, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[107] = new Operation("BIT 5,E", cpu -> cpu.BIT(5, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[108] = new Operation("BIT 5,H", cpu -> cpu.BIT(5, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[109] = new Operation("BIT 5,L", cpu -> cpu.BIT(5, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[110] = new Operation("BIT 5,(HL)", cpu -> cpu.BIT(5, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[111] = new Operation("BIT 5,A", cpu -> cpu.BIT(5, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[112] = new Operation("BIT 6,B", cpu -> cpu.BIT(6, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[113] = new Operation("BIT 6,C", cpu -> cpu.BIT(6, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[114] = new Operation("BIT 6,D", cpu -> cpu.BIT(6, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[115] = new Operation("BIT 6,E", cpu -> cpu.BIT(6, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[116] = new Operation("BIT 6,H", cpu -> cpu.BIT(6, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[117] = new Operation("BIT 6,L", cpu -> cpu.BIT(6, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[118] = new Operation("BIT 6,(HL)", cpu -> cpu.BIT(6, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[119] = new Operation("BIT 6,A", cpu -> cpu.BIT(6, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[120] = new Operation("BIT 7,B", cpu -> cpu.BIT(7, cpu.regs.B), 2, "Z 0 1 -", 8);
        CPU.cbOperations[121] = new Operation("BIT 7,C", cpu -> cpu.BIT(7, cpu.regs.C), 2, "Z 0 1 -", 8);
        CPU.cbOperations[122] = new Operation("BIT 7,D", cpu -> cpu.BIT(7, cpu.regs.D), 2, "Z 0 1 -", 8);
        CPU.cbOperations[123] = new Operation("BIT 7,E", cpu -> cpu.BIT(7, cpu.regs.E), 2, "Z 0 1 -", 8);
        CPU.cbOperations[124] = new Operation("BIT 7,H", cpu -> cpu.BIT(7, cpu.regs.H), 2, "Z 0 1 -", 8);
        CPU.cbOperations[125] = new Operation("BIT 7,L", cpu -> cpu.BIT(7, cpu.regs.L), 2, "Z 0 1 -", 8);
        CPU.cbOperations[126] = new Operation("BIT 7,(HL)", cpu -> cpu.BIT(7, cpu.mem.registerLocation(cpu.regs.HL)), 2, "Z 0 1 -", 12);
        CPU.cbOperations[127] = new Operation("BIT 7,A", cpu -> cpu.BIT(7, cpu.regs.A), 2, "Z 0 1 -", 8);
        CPU.cbOperations[128] = new Operation("RES 0,B", cpu -> cpu.RES(0, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[129] = new Operation("RES 0,C", cpu -> cpu.RES(0, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[130] = new Operation("RES 0,D", cpu -> cpu.RES(0, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[131] = new Operation("RES 0,E", cpu -> cpu.RES(0, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[132] = new Operation("RES 0,H", cpu -> cpu.RES(0, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[133] = new Operation("RES 0,L", cpu -> cpu.RES(0, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[134] = new Operation("RES 0,(HL)", cpu -> cpu.RES(0, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[135] = new Operation("RES 0,A", cpu -> cpu.RES(0, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[136] = new Operation("RES 1,B", cpu -> cpu.RES(1, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[137] = new Operation("RES 1,C", cpu -> cpu.RES(1, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[138] = new Operation("RES 1,D", cpu -> cpu.RES(1, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[139] = new Operation("RES 1,E", cpu -> cpu.RES(1, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[140] = new Operation("RES 1,H", cpu -> cpu.RES(1, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[141] = new Operation("RES 1,L", cpu -> cpu.RES(1, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[142] = new Operation("RES 1,(HL)", cpu -> cpu.RES(1, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[143] = new Operation("RES 1,A", cpu -> cpu.RES(1, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[144] = new Operation("RES 2,B", cpu -> cpu.RES(2, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[145] = new Operation("RES 2,C", cpu -> cpu.RES(2, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[146] = new Operation("RES 2,D", cpu -> cpu.RES(2, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[147] = new Operation("RES 2,E", cpu -> cpu.RES(2, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[148] = new Operation("RES 2,H", cpu -> cpu.RES(2, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[149] = new Operation("RES 2,L", cpu -> cpu.RES(2, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[150] = new Operation("RES 2,(HL)", cpu -> cpu.RES(2, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[151] = new Operation("RES 2,A", cpu -> cpu.RES(2, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[152] = new Operation("RES 3,B", cpu -> cpu.RES(3, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[153] = new Operation("RES 3,C", cpu -> cpu.RES(3, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[154] = new Operation("RES 3,D", cpu -> cpu.RES(3, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[155] = new Operation("RES 3,E", cpu -> cpu.RES(3, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[156] = new Operation("RES 3,H", cpu -> cpu.RES(3, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[157] = new Operation("RES 3,L", cpu -> cpu.RES(3, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[158] = new Operation("RES 3,(HL)", cpu -> cpu.RES(3, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[159] = new Operation("RES 3,A", cpu -> cpu.RES(3, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[160] = new Operation("RES 4,B", cpu -> cpu.RES(4, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[161] = new Operation("RES 4,C", cpu -> cpu.RES(4, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[162] = new Operation("RES 4,D", cpu -> cpu.RES(4, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[163] = new Operation("RES 4,E", cpu -> cpu.RES(4, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[164] = new Operation("RES 4,H", cpu -> cpu.RES(4, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[165] = new Operation("RES 4,L", cpu -> cpu.RES(4, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[166] = new Operation("RES 4,(HL)", cpu -> cpu.RES(4, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[167] = new Operation("RES 4,A", cpu -> cpu.RES(4, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[168] = new Operation("RES 5,B", cpu -> cpu.RES(5, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[169] = new Operation("RES 5,C", cpu -> cpu.RES(5, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[170] = new Operation("RES 5,D", cpu -> cpu.RES(5, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[171] = new Operation("RES 5,E", cpu -> cpu.RES(5, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[172] = new Operation("RES 5,H", cpu -> cpu.RES(5, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[173] = new Operation("RES 5,L", cpu -> cpu.RES(5, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[174] = new Operation("RES 5,(HL)", cpu -> cpu.RES(5, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[175] = new Operation("RES 5,A", cpu -> cpu.RES(5, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[176] = new Operation("RES 6,B", cpu -> cpu.RES(6, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[177] = new Operation("RES 6,C", cpu -> cpu.RES(6, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[178] = new Operation("RES 6,D", cpu -> cpu.RES(6, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[179] = new Operation("RES 6,E", cpu -> cpu.RES(6, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[180] = new Operation("RES 6,H", cpu -> cpu.RES(6, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[181] = new Operation("RES 6,L", cpu -> cpu.RES(6, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[182] = new Operation("RES 6,(HL)", cpu -> cpu.RES(6, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[183] = new Operation("RES 6,A", cpu -> cpu.RES(6, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[184] = new Operation("RES 7,B", cpu -> cpu.RES(7, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[185] = new Operation("RES 7,C", cpu -> cpu.RES(7, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[186] = new Operation("RES 7,D", cpu -> cpu.RES(7, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[187] = new Operation("RES 7,E", cpu -> cpu.RES(7, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[188] = new Operation("RES 7,H", cpu -> cpu.RES(7, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[189] = new Operation("RES 7,L", cpu -> cpu.RES(7, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[190] = new Operation("RES 7,(HL)", cpu -> cpu.RES(7, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[191] = new Operation("RES 7,A", cpu -> cpu.RES(7, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[192] = new Operation("SET 0,B", cpu -> cpu.SET(0, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[193] = new Operation("SET 0,C", cpu -> cpu.SET(0, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[194] = new Operation("SET 0,D", cpu -> cpu.SET(0, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[195] = new Operation("SET 0,E", cpu -> cpu.SET(0, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[196] = new Operation("SET 0,H", cpu -> cpu.SET(0, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[197] = new Operation("SET 0,L", cpu -> cpu.SET(0, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[198] = new Operation("SET 0,(HL)", cpu -> cpu.SET(0, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[199] = new Operation("SET 0,A", cpu -> cpu.SET(0, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[200] = new Operation("SET 1,B", cpu -> cpu.SET(1, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[201] = new Operation("SET 1,C", cpu -> cpu.SET(1, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[202] = new Operation("SET 1,D", cpu -> cpu.SET(1, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[203] = new Operation("SET 1,E", cpu -> cpu.SET(1, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[204] = new Operation("SET 1,H", cpu -> cpu.SET(1, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[205] = new Operation("SET 1,L", cpu -> cpu.SET(1, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[206] = new Operation("SET 1,(HL)", cpu -> cpu.SET(1, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[207] = new Operation("SET 1,A", cpu -> cpu.SET(1, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[208] = new Operation("SET 2,B", cpu -> cpu.SET(2, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[209] = new Operation("SET 2,C", cpu -> cpu.SET(2, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[210] = new Operation("SET 2,D", cpu -> cpu.SET(2, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[211] = new Operation("SET 2,E", cpu -> cpu.SET(2, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[212] = new Operation("SET 2,H", cpu -> cpu.SET(2, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[213] = new Operation("SET 2,L", cpu -> cpu.SET(2, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[214] = new Operation("SET 2,(HL)", cpu -> cpu.SET(2, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[215] = new Operation("SET 2,A", cpu -> cpu.SET(2, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[216] = new Operation("SET 3,B", cpu -> cpu.SET(3, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[217] = new Operation("SET 3,C", cpu -> cpu.SET(3, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[218] = new Operation("SET 3,D", cpu -> cpu.SET(3, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[219] = new Operation("SET 3,E", cpu -> cpu.SET(3, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[220] = new Operation("SET 3,H", cpu -> cpu.SET(3, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[221] = new Operation("SET 3,L", cpu -> cpu.SET(3, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[222] = new Operation("SET 3,(HL)", cpu -> cpu.SET(3, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[223] = new Operation("SET 3,A", cpu -> cpu.SET(3, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[224] = new Operation("SET 4,B", cpu -> cpu.SET(4, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[225] = new Operation("SET 4,C", cpu -> cpu.SET(4, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[226] = new Operation("SET 4,D", cpu -> cpu.SET(4, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[227] = new Operation("SET 4,E", cpu -> cpu.SET(4, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[228] = new Operation("SET 4,H", cpu -> cpu.SET(4, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[229] = new Operation("SET 4,L", cpu -> cpu.SET(4, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[230] = new Operation("SET 4,(HL)", cpu -> cpu.SET(4, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[231] = new Operation("SET 4,A", cpu -> cpu.SET(4, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[232] = new Operation("SET 5,B", cpu -> cpu.SET(5, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[233] = new Operation("SET 5,C", cpu -> cpu.SET(5, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[234] = new Operation("SET 5,D", cpu -> cpu.SET(5, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[235] = new Operation("SET 5,E", cpu -> cpu.SET(5, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[236] = new Operation("SET 5,H", cpu -> cpu.SET(5, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[237] = new Operation("SET 5,L", cpu -> cpu.SET(5, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[238] = new Operation("SET 5,(HL)", cpu -> cpu.SET(5, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[239] = new Operation("SET 5,A", cpu -> cpu.SET(5, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[240] = new Operation("SET 6,B", cpu -> cpu.SET(6, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[241] = new Operation("SET 6,C", cpu -> cpu.SET(6, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[242] = new Operation("SET 6,D", cpu -> cpu.SET(6, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[243] = new Operation("SET 6,E", cpu -> cpu.SET(6, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[244] = new Operation("SET 6,H", cpu -> cpu.SET(6, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[245] = new Operation("SET 6,L", cpu -> cpu.SET(6, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[246] = new Operation("SET 6,(HL)", cpu -> cpu.SET(6, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[247] = new Operation("SET 6,A", cpu -> cpu.SET(6, cpu.regs.A), 2, "- - - -", 8);
        CPU.cbOperations[248] = new Operation("SET 7,B", cpu -> cpu.SET(7, cpu.regs.B), 2, "- - - -", 8);
        CPU.cbOperations[249] = new Operation("SET 7,C", cpu -> cpu.SET(7, cpu.regs.C), 2, "- - - -", 8);
        CPU.cbOperations[250] = new Operation("SET 7,D", cpu -> cpu.SET(7, cpu.regs.D), 2, "- - - -", 8);
        CPU.cbOperations[251] = new Operation("SET 7,E", cpu -> cpu.SET(7, cpu.regs.E), 2, "- - - -", 8);
        CPU.cbOperations[252] = new Operation("SET 7,H", cpu -> cpu.SET(7, cpu.regs.H), 2, "- - - -", 8);
        CPU.cbOperations[253] = new Operation("SET 7,L", cpu -> cpu.SET(7, cpu.regs.L), 2, "- - - -", 8);
        CPU.cbOperations[254] = new Operation("SET 7,(HL)", cpu -> cpu.SET(7, cpu.mem.registerLocation(cpu.regs.HL)), 2, "- - - -", 16);
        CPU.cbOperations[255] = new Operation("SET 7,A", cpu -> cpu.SET(7, cpu.regs.A), 2, "- - - -", 8);
        (this.mem = mem).setCPU(this);
    }
    
    public void setMMU(final MMU mmu) {
        this.mem = mmu;
    }
    
    public int getClockCycles() {
        return this.clockCycles;
    }
    
    public int getClockCycleDelta() {
        return this.clockCycleDelta;
    }
    
    public void coreDump() {
        final int opcode = this.mem.readByte(this.regs.PC.read());
        final Operation op = CPU.operations[opcode];
        final int currentPC = this.regs.PC.read();
        System.out.println("CORE DUMP???");
        this.regs.dump();
    }
    
    public void interrupt(final int handle) {
        this.interrupted = true;
        this.pendingInterrupt = handle;
    }
    
    public void executeOneInstruction(final boolean printOutput, final boolean haltEnabled) {
        this.clockCycleDelta = 0;
        if (this.halted && haltEnabled) {
            this.clockCycleDelta = 4;
            this.serviceInterrupts();
            GameBoy.getInstance().clockTick(this.clockCycleDelta);
            return;
        }
        GameBoy.getInstance().resetClocks();
        final int opcode = this.mem.slowReadByte(this.regs.PC.read());
        final Operation op = CPU.operations[opcode];
        if(opcode != 0) System.out.println(opcode + " | " + op.description + " | " + this.regs.PC.read());

        if(this.regs.PC.read() == 65530) {
              System.out.println("AF : " + this.regs.AF.read());
              System.out.println("BC : " + this.regs.BC.read());
              System.out.println("DE : " + this.regs.DE.read());
              System.out.println("HL : " + this.regs.HL.read());
              System.out.println("SP : " + this.regs.SP.read());

              System.out.println("A : " + this.regs.A.read());
              System.out.println("B : " + this.regs.B.read());
              System.out.println("C : " + this.regs.C.read());
              System.out.println("D : " + this.regs.D.read());
              System.out.println("E : " + this.regs.E.read());
              System.out.println("F : " + this.regs.F.read());
              System.out.println("H : " + this.regs.H.read());
              System.out.println("L : " + this.regs.L.read());

        }
        final int currentPC = this.regs.PC.read();
        final int result = op.execute(this);
        if (GameBoy.getInstance().getClocks() < this.clockCycleDelta) {
            GameBoy.getInstance().clockTick(this.clockCycleDelta - GameBoy.getInstance().getClocks());
        }
        else if (GameBoy.getInstance().getClocks() > this.clockCycleDelta) {
          System.out.println("We tried to do STUFF");
          int a = 1/0;
        }
        if (printOutput) {
          System.out.println("We tried to do STUFF that should be IMPOSSIBLE");
          int a = 1/0;
            System.out.println(this.clockCycleDelta);
            this.regs.dump();
        }
    }
    
    void serviceInterrupts() {
        if (this.interrupted) {
            this.interrupted = false;
            this.halted = false;
            final int interruptVector = this.pendingInterrupt;
            if (interruptVector != -1) {
              System.out.println(this.regs.PC);
              System.out.println(interruptVector);

              System.out.println("AF : " + this.regs.AF.read());
              System.out.println("BC : " + this.regs.BC.read());
              System.out.println("DE : " + this.regs.DE.read());
              System.out.println("HL : " + this.regs.HL.read());

              System.out.println("A : " + this.regs.A.read());
              System.out.println("B : " + this.regs.B.read());
              System.out.println("C : " + this.regs.C.read());
              System.out.println("D : " + this.regs.D.read());
              System.out.println("E : " + this.regs.E.read());
              System.out.println("F : " + this.regs.F.read());
              System.out.println("H : " + this.regs.H.read());
              System.out.println("L : " + this.regs.L.read());
                this.clockCycleDelta += 12;
                this.PUSH(this.regs.PC);
                this.regs.PC.write(interruptVector);
                this.interruptHandler.setInterruptsEnabled(false);
            }
        }
    }
    
    Readable d8() {
        final int value = this.mem.slowReadByte(this.regs.PC.read() + 1);
        return new Readable() {
            @Override
            public int read() {
                return value;
            }
        };
    }
    
    Readable r8() {
        final int value = (byte)this.mem.slowReadByte(this.regs.PC.read() + 1);
        return new Readable() {
            @Override
            public int read() {
                return value;
            }
        };
    }
    
    Readable a8() {
        final int value = 65280 + this.mem.slowReadByte(this.regs.PC.read() + 1);
        return new Readable() {
            @Override
            public int read() {
                return value;
            }
        };
    }
    
    Readable d16() {
        final int value = this.mem.slowReadWord(this.regs.PC.read() + 1);
        return new Readable() {
            @Override
            public int read() {
                return value;
            }
        };
    }
    
    Readable SPr8() {
        final byte r8 = (byte)this.mem.slowReadByte(this.regs.PC.read() + 1);
        final int spVal = this.regs.SP.read();
        final int address = spVal + r8;
        if (r8 >= 0) {
            this.regs.flags.setFlag(5, (spVal & 0xF) + (r8 & 0xF) > 15);
            this.regs.flags.setFlag(4, (spVal & 0xFF) + r8 > 255);
        }
        else {
            this.regs.flags.setFlag(5, (address & 0xF) <= (spVal & 0xF));
            this.regs.flags.setFlag(4, (address & 0xFF) <= (spVal & 0xFF));
        }
        return new Readable() {
            @Override
            public int read() {
                return address;
            }
        };
    }
    
    Readable a16() {
        return this.d16();
    }
    
    ReadWritable selfIncrement(final LongRegister reg) {
        return new ReadWritable() {
            boolean incremented = false;
            
            @Override
            public int read() {
                final int val = reg.read();
                if (!this.incremented) {
                    this.incremented = true;
                    reg.write(val + 1);
                }
                return val;
            }
            
            @Override
            public void write(final int val) {
                if (!this.incremented) {
                    this.incremented = true;
                    reg.write(val + 1);
                }
                else {
                    reg.write(val);
                }
            }
        };
    }
    
    ReadWritable selfDecrement(final LongRegister reg) {
        return new ReadWritable() {
            boolean decremented = false;
            
            @Override
            public int read() {
                final int val = reg.read();
                if (!this.decremented) {
                    this.decremented = true;
                    reg.write(val - 1);
                }
                return val;
            }
            
            @Override
            public void write(final int val) {
                if (!this.decremented) {
                    this.decremented = true;
                    reg.write(val - 1);
                }
                else {
                    reg.write(val);
                }
            }
        };
    }
    
    boolean evaluateCondition(final Condition c) {
        switch (c) {
            case NZ: {
                return !this.regs.flags.getFlag(7);
            }
            case Z: {
                return this.regs.flags.getFlag(7);
            }
            case NC: {
                return !this.regs.flags.getFlag(4);
            }
            case C: {
                return this.regs.flags.getFlag(4);
            }
            default: {
                throw new InvalidParameterException("this shouldn't happen");
            }
        }
    }
    
    int XXX() {
        throw new IllegalArgumentException("invalid opcode");
    }
    
    int LD(final Writable dest, final Readable src) {
        final int val = src.read();
        if (dest instanceof MMU.Location && src == this.regs.SP) {
            ((MMU.Location)dest).writeLong(val);
        }
        else {
            dest.write(val);
        }
        return val;
    }
    
    int PUSH(final LongRegister reg) {
        int sp = this.regs.SP.read();
        --sp;
        this.mem.slowWriteByte(sp, reg.upperByte.read());
        --sp;
        this.mem.slowWriteByte(sp, reg.lowerByte.read());
        this.regs.SP.write(sp);
        return reg.read();
    }
    
    int POP(final LongRegister reg) {
        int sp = this.regs.SP.read();
        if (reg.lowerByte == this.regs.F) {
            reg.lowerByte.write(this.mem.slowReadByte(sp) & 0xFFFFFFF0);
        }
        else {
            reg.lowerByte.write(this.mem.slowReadByte(sp));
        }
        ++sp;
        reg.upperByte.write(this.mem.slowReadByte(sp));
        ++sp;
        this.regs.SP.write(sp);
        return reg.read();
    }
    
    int ADD(final Register dest, final Readable src) {
        final int op1 = src.read();
        final int op2 = dest.read();
        final int halfMask = (dest instanceof LongRegister) ? 4095 : 15;
        final int fullMask = (dest instanceof LongRegister) ? 65535 : 255;
        final int sum = op1 + op2;
        final int result = sum & fullMask;
        this.regs.flags.setFlag(7, result == 0);
        if (dest == this.regs.SP) {
            final int r8 = op1;
            final int spVal = op2;
            final int address = result;
            if (r8 >= 0) {
                this.regs.flags.setFlag(5, (spVal & 0xF) + (r8 & 0xF) > 15);
                this.regs.flags.setFlag(4, (spVal & 0xFF) + r8 > 255);
            }
            else {
                this.regs.flags.setFlag(5, (address & 0xF) <= (spVal & 0xF));
                this.regs.flags.setFlag(4, (address & 0xFF) <= (spVal & 0xFF));
            }
        }
        else {
            this.regs.flags.setFlag(4, sum != result);
            this.regs.flags.setFlag(5, (op1 & halfMask) + (op2 & halfMask) > halfMask);
        }
        dest.write(result);
        return result;
    }
    
    int ADC(final Register dest, final Readable src) {
        final int op1 = src.read();
        final int op2 = dest.read();
        final int halfMask = (dest instanceof LongRegister) ? 4095 : 15;
        final int fullMask = (dest instanceof LongRegister) ? 65535 : 255;
        final int carry = this.regs.flags.getFlag(4) ? 1 : 0;
        final int sum = op1 + op2 + carry;
        final int result = sum & fullMask;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.flags.setFlag(4, sum != result);
        this.regs.flags.setFlag(5, (op1 & halfMask) + (op2 & halfMask) + carry > halfMask);
        dest.write(result);
        return result;
    }
    
    int SUB(final Readable toSubtract) {
        final int op1 = this.regs.A.read();
        final int op2 = toSubtract.read();
        final int diff = op1 - op2;
        final int result = diff & 0xFF;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.flags.setFlag(4, diff < 0);
        this.regs.flags.setFlag(5, (op1 & 0xF) - (op2 & 0xF) < 0);
        this.regs.A.write(result);
        return result;
    }
    
    int SBC(final Readable toSubtract) {
        final int op1 = this.regs.A.read();
        final int op2 = toSubtract.read();
        final int carry = this.regs.flags.getFlag(4) ? 1 : 0;
        final int diff = op1 - op2 - carry;
        final int result = diff & 0xFF;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.flags.setFlag(4, diff < 0);
        this.regs.flags.setFlag(5, (op1 & 0xF) - (op2 & 0xF) - carry < 0);
        this.regs.A.write(result);
        return result;
    }
    
    int AND(final Readable op) {
        final int op2 = this.regs.A.read();
        final int op3 = op.read();
        if ((op3 & 0xFF) != op3) {
            throw new InvalidParameterException("operand must be byte");
        }
        final int result = op2 & op3;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.A.write(result);
        return result;
    }
    
    int OR(final Readable op) {
        final int op2 = this.regs.A.read();
        final int op3 = op.read();
        if ((op3 & 0xFF) != op3) {
            throw new InvalidParameterException("operand must be byte");
        }
        final int result = op2 | op3;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.A.write(result);
        return result;
    }
    
    int XOR(final Readable op) {
        final int op2 = this.regs.A.read();
        final int op3 = op.read();
        if ((op3 & 0xFF) != op3) {
            throw new InvalidParameterException("operand must be byte");
        }
        final int result = op2 ^ op3;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.A.write(result);
        return result;
    }
    
    int CP(final Readable n) {
        final int originalA = this.regs.A.read();
        final int result = this.SUB(n);
        this.regs.A.write(originalA);
        return result;
    }
    
    int INC(final ReadWritable toInc) {
        final int original = toInc.read();
        final int result = original + 1;
        final int fullMask = (toInc instanceof LongRegister) ? 65535 : 255;
        final int halfMask = (toInc instanceof LongRegister) ? 255 : 15;
        this.regs.flags.setFlag(7, (result & fullMask) == 0x0);
        this.regs.flags.setFlag(5, (original & halfMask) + 1 > halfMask);
        toInc.write(result);
        return result;
    }
    
    int DEC(final ReadWritable toDec) {
        final int original = toDec.read();
        final int result = original - 1;
        final int halfMask = (toDec instanceof LongRegister) ? 255 : 15;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.flags.setFlag(5, (original & halfMask) < 1);
        toDec.write(result);
        return result;
    }
    
    int SWAP(final ReadWritable op) {
        final int original = op.read();
        if ((original & 0xFF) != original) {
            throw new InvalidParameterException("operand must be byte");
        }
        final int upperNibble = (original & 0xF0) >> 4;
        final int lowerNibble = original & 0xF;
        final int result = lowerNibble << 4 | upperNibble;
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int DAA() {
        int result;
        final int original = result = this.regs.A.read();
        if (!this.regs.flags.getFlag(6)) {
            if (this.regs.flags.getFlag(4) || original > 153) {
                result += 96;
                this.regs.flags.setFlag(4, true);
            }
            if (this.regs.flags.getFlag(5) || (original & 0xF) > 9) {
                result += 6;
            }
        }
        else {
            if (this.regs.flags.getFlag(4)) {
                result -= 96;
            }
            if (this.regs.flags.getFlag(5)) {
                result -= 6;
            }
        }
        result &= 0xFF;
        this.regs.flags.setFlag(7, result == 0);
        this.regs.A.write(result);
        return result;
    }
    
    int CPL() {
        final int original = this.regs.A.read();
        final int result = ~original & 0xFF;
        this.regs.A.write(result);
        return result;
    }
    
    int CCF() {
        this.regs.flags.setFlag(4, !this.regs.flags.getFlag(4));
        return 0;
    }
    
    int SCF() {
        this.regs.flags.setFlag(4, true);
        return 0;
    }
    
    int NOP() {
        return 0;
    }
    
    int HALT() {
        this.halted = true;
        return 0;
    }
    
    int STOP() {
        this.halted = true;
        return 0;
    }
    
    int DI() {
        this.interruptHandler.setInterruptsEnabled(false);
        return 0;
    }
    
    int EI() {
        this.interruptHandler.setInterruptsEnabled(true);
        return 1;
    }
    
    int RLCA() {
        return this.RLC(this.regs.A);
    }
    
    int RLC(final ReadWritable op) {
        final int original = op.read();
        final int bit7 = original >> 7 & 0x1;
        this.regs.flags.setFlag(4, bit7 == 1);
        final int result = original << 1 | bit7;
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int RLA() {
        return this.RL(this.regs.A);
    }
    
    int RL(final ReadWritable op) {
        final int original = op.read();
        final int bit7 = original >> 7 & 0x1;
        final int carryBit = this.regs.flags.getFlag(4) ? 1 : 0;
        final int result = (original << 1 | carryBit) & 0xFF;
        this.regs.flags.setFlag(4, bit7 == 1);
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int RRCA() {
        return this.RRC(this.regs.A);
    }
    
    int RRC(final ReadWritable op) {
        final int original = op.read();
        final int bit0 = original & 0x1;
        this.regs.flags.setFlag(4, bit0 == 1);
        final int result = original >> 1 | bit0 << 7;
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int RRA() {
        return this.RR(this.regs.A);
    }
    
    int RR(final ReadWritable op) {
        final int original = op.read();
        final int bit0 = original & 0x1;
        final int carryBit = this.regs.flags.getFlag(4) ? 1 : 0;
        final int result = original >> 1 | carryBit << 7;
        this.regs.flags.setFlag(4, bit0 == 1);
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int SLA(final ReadWritable op) {
        final int original = op.read();
        final int bit7 = original >> 7 & 0x1;
        final int result = original << 1 & 0xFF;
        this.regs.flags.setFlag(4, bit7 == 1);
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int SRA(final ReadWritable op) {
        final int original = op.read();
        final int bit0 = original & 0x1;
        final int bit2 = original >> 7 & 0x1;
        final int result = (original >> 1 | bit2 << 7) & 0xFF;
        this.regs.flags.setFlag(4, bit0 == 1);
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int SRL(final ReadWritable op) {
        final int original = op.read();
        final int bit0 = original & 0x1;
        final int result = original >> 1;
        this.regs.flags.setFlag(4, bit0 == 1);
        this.regs.flags.setFlag(7, result == 0);
        op.write(result);
        return result;
    }
    
    int BIT(final int bitnum, final Readable op) {
        final int val = op.read();
        this.regs.flags.setFlag(7, (val >> bitnum & 0x1) == 0x0);
        return val;
    }
    
    int SET(final int bitnum, final ReadWritable op) {
        int val = op.read();
        val |= 1 << bitnum;
        op.write(val);
        return val;
    }
    
    int RES(final int bitnum, final ReadWritable op) {
        int val = op.read();
        val &= ~(1 << bitnum);
        op.write(val);
        return val;
    }
    
    int JP(final Readable jumpLocation) {
        final int location = jumpLocation.read();
        this.regs.PC.write(location);
        return 1;
    }
    
    int JP(final Condition cond, final Readable jumpLocation) {
        if (this.evaluateCondition(cond)) {
            return this.JP(jumpLocation);
        }
        return -1;
    }
    
    int JR(final Readable offset) {
        final int location = this.regs.PC.read() + (byte)offset.read();
        this.regs.PC.write(location);
        return 0;
    }
    
    int JR(final Condition cond, final Readable offset) {
        if (this.evaluateCondition(cond)) {
            return this.JR(offset);
        }
        return -1;
    }
    
    int CALL(final Readable jumpLocation) {
        final int nextPC = this.regs.PC.read() + 3;
        final LongRegister temp = new LongRegister();
        temp.write(nextPC);
        this.PUSH(temp);
        return this.JP(jumpLocation);
    }
    
    int CALL(final Condition cond, final Readable jumpLocation) {
        if (this.evaluateCondition(cond)) {
            return this.CALL(jumpLocation);
        }
        return -1;
    }
    
    int RST(final int n) {
        final LongRegister nextPC = new LongRegister();
        nextPC.write(this.regs.PC.read() + 1);
        this.PUSH(nextPC);
        final LongRegister temp = new LongRegister();
        temp.write(n);
        return this.JP(temp);
    }
    
    int RET() {
        final LongRegister temp = new LongRegister();
        this.POP(temp);
        return this.JP(temp);
    }
    
    int RET(final Condition cond) {
        if (this.evaluateCondition(cond)) {
            return this.RET();
        }
        return -1;
    }
    
    int RETI() {
        this.EI();
        return this.RET();
    }
    
    static {
        CPU.operations = new Operation[256];
        CPU.cbOperations = new Operation[256];
    }
    
    static class Operation
    {
        String description;
        Lambda lambda;
        int ticks;
        int length;
        String flagsAffected;
        
        public Operation(final String description, final Lambda lambda, final int length, final String flagsAffected, final int ticks) {
            this.description = description;
            this.lambda = lambda;
            this.ticks = ticks;
            this.length = length;
            this.flagsAffected = flagsAffected;
        }
        
        protected void handleFlagsWritable(final CPU cpu) {
            final int[] flags = { 7, 6, 5, 4 };
            final boolean[] writable = new boolean[8];
            for (int i = 0; i < this.flagsAffected.length(); i += 2) {
                final char descriptor = this.flagsAffected.charAt(i);
                final int flag = flags[i / 2];
                switch (descriptor) {
                    case '-':
                    case '0':
                    case '1': {
                        writable[flag] = false;
                        break;
                    }
                    default: {
                        writable[flag] = true;
                        break;
                    }
                }
            }
            cpu.regs.flags.enableFlagWrites(writable[7], writable[6], writable[5], writable[4]);
        }
        
        protected void handleFlagsValues(final CPU cpu) {
            final int[] flags = { 7, 6, 5, 4 };
            cpu.regs.flags.enableFlagWrites(true, true, true, true);
            for (int i = 0; i < this.flagsAffected.length(); i += 2) {
                final char descriptor = this.flagsAffected.charAt(i);
                final int flag = flags[i / 2];
                switch (descriptor) {
                    case '0': {
                        cpu.regs.flags.setFlag(flag, false);
                        break;
                    }
                    case '1': {
                        cpu.regs.flags.setFlag(flag, true);
                        break;
                    }
                }
            }
        }
        
        public int execute(final CPU cpu) {
            this.handleFlagsWritable(cpu);
            final int result = this.lambda.exec(cpu);
            this.handleFlagsValues(cpu);
            cpu.clockCycles += this.ticks;
            cpu.clockCycleDelta += this.ticks;
            cpu.regs.PC.write(cpu.regs.PC.read() + this.length);
            cpu.serviceInterrupts();
            return result;
        }
    }
    
    static class Jump extends Operation
    {
        int ticksIfJumped;
        int ticksIfNotJumped;
        
        public Jump(final String description, final Lambda lambda, final int length, final String flagsAffected, final int ticksIfJumped, final int ticksIfNotJumped) {
            super(description, lambda, length, flagsAffected, ticksIfJumped);
            this.ticksIfJumped = ticksIfJumped;
            this.ticksIfNotJumped = ticksIfNotJumped;
        }
        
        @Override
        public int execute(final CPU cpu) {
            this.handleFlagsWritable(cpu);
            final int result = this.lambda.exec(cpu);
            this.handleFlagsValues(cpu);
            if (result == 0 || result == -1) {
                cpu.regs.PC.write(cpu.regs.PC.read() + this.length);
            }
            if (result == -1) {
                cpu.clockCycles += this.ticksIfNotJumped;
                cpu.clockCycleDelta += this.ticksIfNotJumped;
            }
            else {
                cpu.clockCycles += this.ticksIfJumped;
                cpu.clockCycleDelta += this.ticksIfJumped;
            }
            cpu.serviceInterrupts();
            return result;
        }
    }
    
    static class CB extends Operation
    {
        public CB() {
            super("CB", null, 2, "Z N H C", 4);
        }
        
        @Override
        public int execute(final CPU cpu) {
            final int cbOpcode = cpu.mem.slowReadByte(cpu.regs.PC.read() + 1);
            final Operation cbOperation = CPU.cbOperations[cbOpcode];
            final int result = cbOperation.execute(cpu);
            return result;
        }
    }
    
    enum Condition
    {
        NZ, 
        Z, 
        NC, 
        C;
    }
}
