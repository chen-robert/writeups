main: main.c
	gcc -masm=intel -no-pie -o main main.c
	gcc -masm=intel -no-pie -o unstripped main.c
	strip main 

test: test.c
	gcc -masm=intel -o main test.c
	gcc -masm=intel -o unstripped test.c
	strip main 
