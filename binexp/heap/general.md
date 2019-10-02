# Some General Tips
- [unsorted bin attack](https://github.com/shellphish/how2heap/blob/master/glibc_2.26/unsorted_bin_attack.c) along with [corrupting fastbin pointers](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/fastbin_dup_into_stack.c) leads to arbitrary write
- overwriting `__free_hook` and then freeing `;sh;` can be more reliable way to get a shell
- don't get too caught up the big picture. remember than functions execute instructions one line at a time. 
- partial overwrites are very common
- don't get caught up in thinking of everything as qwords. at the low level, everything is a byte. 

## One-Gadgets
- you can trigger malloc printerror with double free to trigger `__malloc_hook`. See [here for more info](https://blog.osiris.cyber.nyu.edu/2017/09/30/csaw-ctf-2017-auir/)
- rax constraint is usually hard to satisfy. see if you can clean up the stack with null bytes to satisfy the `[$rsp + X]` gadgets
