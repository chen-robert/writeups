// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.util.HashMap;
import java.io.Serializable;

public class InterruptHandler implements Serializable
{
    private static final long serialVersionUID = -2641142498470471980L;
    private CPU cpu;
    public static final int VBLANK = 64;
    public static final int LCDC = 72;
    public static final int TIMER_OVERFLOW = 80;
    public static final int SERIAL_COMPLETION = 88;
    public static final int JOYPAD = 96;
    public HashMap<Integer, Boolean> specificEnabled;
    private boolean interruptsEnabled;
    
    public void setInterruptsEnabled(final boolean interruptsEnabled) {
        this.interruptsEnabled = interruptsEnabled;
    }
    
    public void setSpecificEnabled(final int handle, final boolean enabled) {
        this.specificEnabled.put(handle, enabled);
    }
    
    public InterruptHandler(final CPU cpu) {
        (this.specificEnabled = new HashMap<Integer, Boolean>()).put(64, false);
        this.specificEnabled.put(72, false);
        this.specificEnabled.put(80, false);
        this.specificEnabled.put(88, false);
        this.specificEnabled.put(96, false);
        this.interruptsEnabled = false;
        this.cpu = cpu;
    }
    
    public boolean issueInterruptIfEnabled(final int handle) {
        if (!this.interruptsEnabled) {
            this.cpu.interrupt(-1);
            return false;
        }
        if (!this.specificEnabled.getOrDefault(handle, false)) {
            return false;
        }
        this.cpu.interrupt(handle);
        return true;
    }
    
    public boolean handleIF(int IFflag) {
        if ((IFflag & 0x1) == 0x1) {
            return this.issueInterruptIfEnabled(64);
        }
        IFflag >>= 1;
        if ((IFflag & 0x1) == 0x1) {
            return this.issueInterruptIfEnabled(72);
        }
        IFflag >>= 1;
        if ((IFflag & 0x1) == 0x1) {
            return this.issueInterruptIfEnabled(80);
        }
        IFflag >>= 1;
        if ((IFflag & 0x1) == 0x1) {
            return this.issueInterruptIfEnabled(88);
        }
        IFflag >>= 1;
        if ((IFflag & 0x1) == 0x1) {
            this.issueInterruptIfEnabled(96);
        }
        return false;
    }
    
    public void handleIE(int IEflag) {
        this.setSpecificEnabled(64, (IEflag & 0x1) == 0x1);
        IEflag >>= 1;
        this.setSpecificEnabled(72, (IEflag & 0x1) == 0x1);
        IEflag >>= 1;
        this.setSpecificEnabled(80, (IEflag & 0x1) == 0x1);
        IEflag >>= 1;
        this.setSpecificEnabled(88, (IEflag & 0x1) == 0x1);
        IEflag >>= 1;
        this.setSpecificEnabled(96, (IEflag & 0x1) == 0x1);
    }
    
    @Override
    public String toString() {
        if (!this.interruptsEnabled) {
            return "IME OFF";
        }
        return this.specificEnabled.toString();
    }
}
