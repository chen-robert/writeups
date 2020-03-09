// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.io.Serializable;

public class MMU implements Serializable
{
    public byte[] mem;
    private Joypad joypad;
    private int charsPrinted;
    private CPU cpu;
    
    public MMU() {
        this.mem = new byte[65536];
        this.charsPrinted = 0;
    }
    
    public void setCPU(final CPU cpu) {
        this.cpu = cpu;
    }
    
    public CPU getCPU() {
        return this.cpu;
    }
    
    public int slowReadByte(final int location) {
        GameBoy.getInstance().clockTick(4L);
        return this.readByte(location);
    }
    
    public void setJoypad(final Joypad joypad) {
        this.joypad = joypad;
    }
    
    public int readByte(final int location) {
        if (location != 65280) {
            return this.mem[location & 0xFFFF] & 0xFF;
        }
        if (BitOps.extract(this.mem[65280] & 0xFF, 5, 5) == 0L) {
            return this.joypad.readButtons();
        }
        if (BitOps.extract(this.mem[65280] & 0xFF, 4, 4) == 0L) {
            return this.joypad.readDirections();
        }
        return 255;
    }
    
    public int slowReadWord(final int location) {
        return (this.slowReadByte(location + 1) << 8) + this.slowReadByte(location);
    }
    
    public int readWord(final int location) {
        return (this.readByte(location + 1) << 8) + this.readByte(location);
    }
    
    public void slowWriteByte(final int location, final int toWrite) {
        GameBoy.getInstance().clockTick(4L);
        this.writeByte(location, toWrite);
    }
    
    public void writeByte(final int location, final int toWrite) {
        if (location == 65281) {
            System.out.printf("%c", toWrite & 0xFF);
            ++this.charsPrinted;
            if (this.charsPrinted > 30) {
                System.out.println("\noutput limit exceeded");
                System.exit(0);
            }
            return;
        }
        if (location < 65408) {
            return;
        }
        if (location == 65535) {
            this.cpu.interruptHandler.handleIE(toWrite & 0xFF);
        }
        System.out.println("WRITE: " + location + " -> " + (toWrite & 0xFF));
        this.mem[location] = (byte)(toWrite & 0xFF);
    }
    
    public void writeWord(final int location, int toWrite) {
        toWrite &= 0xFFFF;
        this.writeByte(location, toWrite & 0xFF);
        this.writeByte(location + 1, toWrite >> 8);
    }
    
    public Location shortRegisterLocation(final Register r) {
        return new Location(65280 + r.read());
    }
    
    public Location registerLocation(final Readable r) {
        return new Location(r.read());
    }
    
    public ReadWritable a8Location(final Register pc) {
        int address = 65280;
        address += this.slowReadByte(pc.read() + 1);
        return new Location(address);
    }
    
    public ReadWritable a16Location(final Register pc) {
        final int address = this.slowReadWord(pc.read() + 1);
        return new Location(address);
    }
    
    public void writeBytes(final int location, final byte[] sequence) {
        for (int i = 0; i < sequence.length; ++i) {
            this.writeByte(location + i, sequence[i]);
        }
    }
    
    class Location implements ReadWritable
    {
        private int address;
        
        public Location(final int address) {
            this.address = address;
        }
        
        @Override
        public int read() {
            return MMU.this.slowReadByte(this.address);
        }
        
        @Override
        public void write(final int val) {
            MMU.this.slowWriteByte(this.address, val);
        }
        
        public void writeLong(final int val) {
            MMU.this.slowWriteByte(this.address, val & 0xFF);
            MMU.this.slowWriteByte(this.address + 1, val >> 8 & 0xFF);
        }
    }
}
