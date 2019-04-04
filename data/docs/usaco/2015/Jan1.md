### [Fort Moo](http://usaco.org/index.php?page=viewproblem2&cpid=600)

##### Problem Statement
>Bessie has already chosen a site on which to build the fort -- a piece of land measuring N meters by M meters (1≤N,M≤200). Unfortunately, the site has some swampy areas that cannot be used to support the frame. Please help Bessie determine the largest area she can cover with her fort (the area of the rectangle supported by the frame), such that the frame avoids sitting on any of the swampy areas.

Note the very generous bounds on **N** and **M**. This implies an **O(N^3)** solution will suffice.

##### Naive Solution
Note a naive solution which runs in **O(N^4)** can be achieved through the use of a lookup table. If we precompute the sums from **0...i** for each row **j**, we can easily check if there is a swamp in the range **(a,b)** in row **j**. The precomputed sums should be equal; `lp[j][a] == lp[j][b]`. This is an **O(1)** check and can similarly be applied to columns. The remaining **O(4)** is spent on looping through all possible pairs of opposite corners. 

##### Sliding Window
We only have to improve this runtime by **O(N)**. To do this, we use a sliding window. 

In our outer loop, we iterate through all possible combinations of rows. In the inner loop, we maintain two pointer s**a** and **b** for our sliding window.

The key observation to make is that if there is a swamp between some **(a, b)** horizontally, we have to move **a** up to that swamp's position. Otherwise, there will still be a swamp in the interval **(a, b)**. 

More specifically, anytime there is a swamp at pointer **b**, we must move **a** to **b**. 

This optimization reduces the runtime to **O(N^3)**. 

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/fortmoo.java)