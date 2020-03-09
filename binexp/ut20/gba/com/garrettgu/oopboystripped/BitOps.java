// 
// Decompiled by Procyon v0.5.36
// 

package com.garrettgu.oopboystripped;

public class BitOps
{
    static long extract(final long in, final int left, final int right) {
        final int leftShift = 63 - left;
        return in << leftShift >>> leftShift + right;
    }
}
