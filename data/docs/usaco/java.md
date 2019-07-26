# Java Tricks

Honestly, you should switch to c++. But if you insist on using Java, here are a few tricks I picked up over the years.

## Memory

Memory allocation is extremely cheap (~1e6 bytes per 1ms) compared to everything else - don't be afraid to allocate huge arrays. That being said, be careful you don't hit a MLE.

Be careful of the dimensional order of 2D arrays.

```java
int[][] memory = new int[(int) 1e7][3]
```

is 10 million arrays of length 3. The slow part of the allocation is due to the need to create 10 million arrays. Reordering the dimensions to become

```java
int[][] memory = new int[3][(int) 1e7]
```

offers significant performance gains.

## Objects

Object initialization in Java is extremely expensive. If you have to instantate a great deal (more than 1e6) of relatively simple objects (e.g. points), consider inlining their properties in a large 2D array.

```java
static int[][] objects = new int[2][(int) 1e7];
static int cnt;

static int getObject(int x, int y){
  objects[cnt][0] = x;
  objects[cnt][1] = y;

  return cnt++;
}
```

Note the dimensional order of the objects array.
