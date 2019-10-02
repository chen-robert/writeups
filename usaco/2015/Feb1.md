### [Load Balancing](http://usaco.org/index.php?page=viewproblem2&cpid=624)

##### Problem Statement
> Farmer John's N cows are each standing at distinct locations (x1,y1)…(xn,yn) on his two-dimensional farm (`1≤N≤100,000`, and the `xi`'s and `yi`'s are positive odd integers of size at most 1,000,000). FJ wants to partition his field by building a long (effectively infinite-length) north-south fence with equation `x=a` (a will be an even integer, thus ensuring that he does not build the fence through the position of any cow). He also wants to build a long (effectively infinite-length) east-west fence with equation `y=b`, where b is an even integer. These two fences cross at the point (a,b), and together they partition his field into four regions.
FJ wants to choose a and b so that the cows appearing in the four resulting regions are reasonably "balanced", with no region containing too many cows. Letting M be the maximum number of cows appearing in one of the four regions, FJ wants to make M as small as possible. Please help him determine this smallest possible value for M.

In other words, given a set of points, divide them into 4 sections with one horizontal line and one vertical line. Let **M** be the maximum number of cows in the 4 regions. We want to minimize **M**. 

##### Observations 
Because `(1 <= N <= 1e5)`, we probably need an `O(N lg N)` algorithm. 

If we iterate over all possible vertical lines, this costs `O(N)`. We could probably binary search over the two sections in `O(lg N)`. 

As we iterate over the possible vertical lines in order, we keep running counts of the number of points to the left and right of our line. 


##### Solution
Specifically, given two sections `L` and `R`, we want to find the optimal placement of a horizontal line such that **M** is minimized. We can use a BIT to calculate the number of points in `L` and `R` underneath a given horizontal line. 

Let `L_top` be the number of points above a given horizontal line for section `L`. Similarly, define `R_top` for `R`. 

Note that
```
M = max(max(L_top, len(L) - L_top), max(R_top, len(R) - R_top))
```

This function looks like a parabola. By taking derivatives, we can binary search our way to the minimum. (Drawing this out may help you visualize). 

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/balancing.java)