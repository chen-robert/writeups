// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

public class Joypad
{
    private MMU mmu;
    private InterruptHandler interruptHandler;
    private int a;
    private int b;
    private int select;
    private int start;
    private int up;
    private int down;
    private int left;
    private int right;
    
    public Joypad(final MMU mmu, final InterruptHandler interruptHandler) {
        this.mmu = mmu;
        this.interruptHandler = interruptHandler;
        mmu.setJoypad(this);
        this.a = 1;
        this.b = 1;
        this.select = 1;
        this.start = 1;
        this.up = 1;
        this.down = 1;
        this.left = 1;
        this.right = 1;
    }
    
    public void keyPressed(final int code) {
        switch (code) {
            case 37: {
                if (this.left == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.left = 0;
                break;
            }
            case 39: {
                if (this.right == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.right = 0;
                break;
            }
            case 38: {
                if (this.up == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.up = 0;
                break;
            }
            case 40: {
                if (this.down == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.down = 0;
                break;
            }
            case 90: {
                if (this.a == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.a = 0;
                break;
            }
            case 88: {
                if (this.b == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.b = 0;
                break;
            }
            case 10: {
                if (this.start == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.start = 0;
                break;
            }
            case 8:
            case 16: {
                if (this.select == 1) {
                    this.interruptHandler.issueInterruptIfEnabled(96);
                }
                this.select = 0;
                break;
            }
        }
    }
    
    public void keyReleased(final int code) {
        switch (code) {
            case 37: {
                this.left = 1;
                break;
            }
            case 39: {
                this.right = 1;
                break;
            }
            case 38: {
                this.up = 1;
                break;
            }
            case 40: {
                this.down = 1;
                break;
            }
            case 90: {
                this.a = 1;
                break;
            }
            case 88: {
                this.b = 1;
                break;
            }
            case 10: {
                this.start = 1;
                break;
            }
            case 8:
            case 16: {
                this.select = 1;
                break;
            }
        }
    }
    
    public int readDirections() {
        return (this.down << 3) + (this.up << 2) + (this.left << 1) + this.right;
    }
    
    public int readButtons() {
        return (this.start << 3) + (this.select << 2) + (this.b << 1) + this.a;
    }
}
