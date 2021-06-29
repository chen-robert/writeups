#!/bin/sh 
qemu-system-x86_64 \
    -m 64M \
    -s \
    -kernel bzImage \
    -initrd ramfs.cpio \
    -nographic \
    -append "console=ttyS0 quiet nokaslr" \
    -monitor /dev/null
