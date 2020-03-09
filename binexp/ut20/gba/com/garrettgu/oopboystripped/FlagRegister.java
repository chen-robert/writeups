// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

class FlagRegister implements ShortRegister
{
    ShortRegister wrapped;
    
    public FlagRegister(final ShortRegister toWrap) {
        this.wrapped = toWrap;
    }
    
    @Override
    public int read() {
        return this.wrapped.read() & 0xF0;
    }
    
    @Override
    public void write(final int val) {
        this.wrapped.write(val & 0xF0);
    }
    
    @Override
    public String toString() {
        return String.format("%04X", this.read());
    }
}
