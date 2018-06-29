### Your Ride is Here

This is the first problem!

##### Submitting
Remember that you have to include a header before submitting solutions. For this problem, it might looks something like this.

> Note that your id is just your username

```java
/*
ID: your_id_here 
LANG: JAVA
TASK: ride
*/
```


##### IO (Input / Output)

Unlike some other programming contests, input is to be read from files. Specifically, input is read from `problem_name.in` and output is written to `problem_name.out`. 

In Java, we can use `java.util.Scanner` and `java.io.PrintStream` for file IO. 

```java
public static void main(String args[]){
  Scanner in = new Scanner(new File("read.in"));
  PrintStream out = new PrintStream(new File("read.out"));
 
  //Your code goes here 
  
  in.close();
  out.close();
}
```

You can read in the next String from the file with `in.next()`. 

##### Problem Statement 

We first have to read in the two Strings from the file.
```java
String group = in.next();
String comet = in.next();
```
Now we need a function to convert the Strings to a number, following the problem statement. 
> Both the name of the group and the name of the comet are converted into a number in the following manner: the final number is just the product of all the letters in the name, where "A" is 1 and "Z" is 26. For instance, the group "USACO" would be 21 * 19 * 1 * 3 * 15 = 17955. If the group's number mod 47 is the same as the comet's number mod 47, then you need to tell the group to get ready!

##### Char to Int
A nice trick for converting `char` to `int` in Java is subtracting char values. For example, if we wanted to convert "A" to 1, "B" to 2, and so on, we could use
```java
public static int convert(char c){
  return c - 'A' + 1;
}
```
This works because chars are actually just numbers, and thus we can perform arithmatic operations on them. 

The rest of the problem is left as an exercise to the reader. 