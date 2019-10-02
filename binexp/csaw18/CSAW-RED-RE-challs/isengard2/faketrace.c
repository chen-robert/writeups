#include <stdio.h>

int times = -1;
long ptrace(int x, int y, int z)
{
	times++;
	printf("%d", times);
	return times == 0? 0: -1;
}
