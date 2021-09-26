.PHONY: clean all
all: pay

pay: pay.c
	gcc -O3 -static -pthread -Wall -o $@ $^

clean:
	rm -f pay
