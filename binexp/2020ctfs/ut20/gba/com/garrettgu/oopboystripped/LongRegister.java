// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.io.Serializable;

class LongRegister implements Register, Serializable
{
    private static final long serialVersionUID = 2142281106792231516L;
    private int value;
    ShortRegister lowerByte;
    ShortRegister upperByte;
    
    LongRegister() {
        this.lowerByte = new ShortRegister() {
            private static final long serialVersionUID = 1L;
            
            @Override
            public int read() {
                return LongRegister.this.value & 0xFF;
            }
            
            @Override
            public void write(int val) {
                val &= 0xFF;
                final LongRegister this$0 = LongRegister.this;
                this$0.value &= 0xFF00;
                final LongRegister this$2 = LongRegister.this;
                this$2.value |= val;
            }
            
            @Override
            public String toString() {
                return String.format("%02X", this.read());
            }
        };
        this.upperByte = new ShortRegister() {
            private static final long serialVersionUID = 1L;
            
            @Override
            public int read() {
                return (LongRegister.this.value & 0xFF00) >> 8;
            }
            
            @Override
            public void write(int val) {
                val = (val & 0xFF) << 8;
                final LongRegister this$0 = LongRegister.this;
                this$0.value &= 0xFF;
                final LongRegister this$2 = LongRegister.this;
                this$2.value |= val;
            }
            
            @Override
            public String toString() {
                return String.format("%02X", this.read());
            }
        };
    }
    
    @Override
    public int read() {
        return this.value;
    }
    
    @Override
    public void write(final int val) {
        this.value = (val & 0xFFFF);
    }
    
    @Override
    public String toString() {
        return String.format("%04X", this.read());
    }
}
