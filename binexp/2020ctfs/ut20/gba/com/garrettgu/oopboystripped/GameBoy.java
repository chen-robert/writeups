// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

import java.io.FileInputStream;
import java.io.File;
import java.util.Scanner;

public class GameBoy
{
    static GameBoy instance;
    MMU mmu;
    CPU cpu;
    Joypad joypad;
    private long clockTicks;
    private long time;
    
    public GameBoy() {
        this.mmu = new MMU();
        this.cpu = new CPU(this.mmu);
        this.joypad = new Joypad(this.mmu, this.cpu.interruptHandler);
        this.clockTicks = 0L;
        this.time = 0L;
    }
    
    public static GameBoy getInstance() {
        return GameBoy.instance;
    }
    
    public long getClocks() {
        return this.clockTicks;
    }
    
    public void resetClocks() {
        this.clockTicks = 0L;
    }
    
    public void clockTick(final long ticks) {
        this.time += ticks;
        this.clockTicks += ticks;
    }
    
    private int getKeyEvent(final char c) {
        switch (c) {
            case 'u': {
                return 38;
            }
            case 'd': {
                return 40;
            }
            case 'l': {
                return 37;
            }
            case 'r': {
                return 39;
            }
            case 'a': {
                return 90;
            }
            case 'b': {
                return 88;
            }
            case 's': {
                return 10;
            }
            case 'e': {
                return 16;
            }
            default: {
                return 48;
            }
        }
    }
    
    public void main() throws Exception {
        final Scanner fin = new Scanner(System.in);
        final File file = new File("/utctf.gb");
        new FileInputStream(file).read(this.mmu.mem);
        this.cpu.regs.AF.write(432);
        this.cpu.regs.BC.write(19);
        this.cpu.regs.DE.write(216);
        this.cpu.regs.HL.write(333);
        this.cpu.regs.SP.write(65534);
        this.cpu.regs.PC.write(256);
        int currentKey = 48;
        System.out.println("Welcome to the UTCTF Game Boy TAS! ");
        for (int i = 0; i < 12; ++i) {
            System.out.print("Please enter your next command: ");
            final String key = fin.next();
            final int duration = fin.nextInt();
            if (duration > 40000) {
                System.out.println("Duration cannot exceed 40000");
                System.exit(0);
            }
            final int nextKey = this.getKeyEvent(key.charAt(0));
            if (nextKey != currentKey) {
                this.joypad.keyReleased(currentKey);
                this.joypad.keyPressed(nextKey);
                currentKey = nextKey;
            }
            this.time = 0L;
            while (this.time < duration) {
                this.cpu.executeOneInstruction(false, false);
            }
        }
        System.out.println("You ran out of commands");
    }
    
    public static void main(final String[] args) throws Exception {
        GameBoy.instance.main();
    }
    
    static {
        GameBoy.instance = new GameBoy();
    }
}
