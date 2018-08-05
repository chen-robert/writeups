### Picture *IOI 1998*

##### Problem Statement
Given `N (1 <= N < 5000)` rectangles, some of which may be overlapping, find the combined perimeter. 

##### Observations 
The first step is to realize we can process the horizontal and vertical edges separately. That's because we can divide up any perimeter into separate horizontal and vertical components. After we calculate these values separately, we can then combine them again. 

For each rectangle, we extract the 4 edges. This allows us to separate vertical components from horizontal ones.

A common theme for many problems is processing in sorted order. For this problem, it would probably make sense to process the vertical edges from left to right (and the horizontal ones top to bottom). 

Next, note that there are two types of edges. The edges that begin a rectangle, and the edges that signify the end of a rectangle (when we are processing the edges in order). We can differentiate between these two types of edges with a boolean flag, `starting`. 

##### Solution
Assume we have a data structure that supports
 * `O(1)` query # of distinct intervals
 * `O(lg N)` add interval
 * `O(lg N)` delete interval
 
We process the edges in order. If we meet a `starting` edge, we add it to our data structure. Otherwise, we remove it. Let the # of distinct intervals once we've processed edge `i` be `intervals[i]`. 

The total perimeter would be 
``` 
for(i in x_positions):
  perimeter += intervals[i] * (x_positions[i] - x_positions[i-1]) 
```

##### Data Structure
Now we need to construct this magic data structure that will give us 
 * `O(1)` query # of distinct intervals
 * `O(lg N)` add interval
 * `O(lg N)` delete interval

We'll use a segment tree for this. Specifically, each segment has the following properties. 
 * `boolean coversLeft` True if the left side of this interval is filled
 * `boolean coversRight` True if the right side of this interval is filled
 * `int intervalCount` The number of times this interval is covered completely.
 * `int innerIntervals` The number of intervals inside this interval. 

We can recalculate a segment `S`'s values as so. Let `L` and `R` be the left and right children of `S` respectively.

```
if S.intervalCount > 0:
  S.innerIntervals = 0
  S.coversLeft = true
  S.coversRight = true
else:
  S.coversLeft = L.coversLeft
  S.coversRight = R.coversRight
  
  S.innerIntervals = L.innerIntervals + R.innerIntervals 
    + (L.coversRight == R.coversLeft ? 0: 1)
```

We can update `intervalCount` as we typically do for any segment tree. 

The rest of the problem is left as an exercise to the reader. 

