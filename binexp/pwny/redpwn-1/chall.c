int main() {
  puts("What is your name: ");

  char buff[1337] = "";
  gets(buff);

  puts("Nice to meet you, ");
  printf(buff);
}
