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

## Crafted Inputs

Sometimes you can get TLE if organizers submit specifically crafted inputs to achieve worst-case time complexities for certain data structures. For example, java HashSet hash collisions can make operations O(N) instead of O(1). Another example of this can be found in the `Arrays.sort` method. Certain inputs can trigger the `O(N^2)` worst case runtime, timing out an otherwise working solution. To mitigate this, you can use java's `TreeSet` and `TreeMap` classes to guarantee an `O(lg N)` operation. Similarly, you can shuffle your arrays before sorting them.
