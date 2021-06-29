// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.security.InvalidParameterException;
import java.io.Serializable;

public class RegisterFile implements Serializable
{
    private static final long serialVersionUID = 1620775094696906337L;
    public LongRegister AF;
    public LongRegister BC;
    public LongRegister DE;
    public LongRegister HL;
    public LongRegister SP;
    public LongRegister PC;
    public ShortRegister A;
    public ShortRegister F;
    public ShortRegister B;
    public ShortRegister C;
    public ShortRegister D;
    public ShortRegister E;
    public ShortRegister H;
    public ShortRegister L;
    public static final int ZFLAG = 7;
    public static final int NFLAG = 6;
    public static final int HFLAG = 5;
    public static final int CFLAG = 4;
    public FlagSet flags;
    
    public void dump() {
      System.out.println("We tried dumping for some reason????");
      int a = 1/0;
    }
    
    public RegisterFile() {
        this.AF = new LongRegister();
        this.A = this.AF.upperByte;
        this.AF.lowerByte = new FlagRegister(this.AF.lowerByte);
        this.F = this.AF.lowerByte;
        this.BC = new LongRegister();
        this.B = this.BC.upperByte;
        this.C = this.BC.lowerByte;
        this.DE = new LongRegister();
        this.D = this.DE.upperByte;
        this.E = this.DE.lowerByte;
        this.HL = new LongRegister();
        this.H = this.HL.upperByte;
        this.L = this.HL.lowerByte;
        this.SP = new LongRegister();
        this.PC = new LongRegister();
        this.flags = new FlagSet(this.F);
    }
    
    public class FlagSet implements Serializable
    {
        private static final long serialVersionUID = 888159977466716630L;
        private Register flagReg;
        boolean[] flagWritable;
        private boolean ZWritable;
        private boolean NWritable;
        private boolean HWritable;
        private boolean CWritable;
        
        public void enableFlagWrites(final boolean z, final boolean n, final boolean h, final boolean c) {
            this.flagWritable[7] = z;
            this.flagWritable[6] = n;
            this.flagWritable[5] = h;
            this.flagWritable[4] = c;
        }
        
        public FlagSet(final Register r) {
            this.flagWritable = new boolean[8];
            this.ZWritable = true;
            this.NWritable = true;
            this.HWritable = true;
            this.CWritable = true;
            this.flagReg = r;
        }
        
        public boolean getFlag(final int flagNum) {
            if (flagNum < 4) {
                throw new InvalidParameterException("bad flag number");
            }
            return (this.flagReg.read() >> flagNum & 0x1) == 0x1;
        }
        
        public void setFlag(final int flagNum, final boolean val) {
            if (flagNum < 4) {
                throw new InvalidParameterException("bad flag number");
            }
            if (this.flagWritable[flagNum]) {
                int flags = this.flagReg.read();
                if (val) {
                    flags |= 1 << flagNum;
                }
                else {
                    flags &= ~(1 << flagNum);
                }
                this.flagReg.write(flags);
            }
        }
    }
}
