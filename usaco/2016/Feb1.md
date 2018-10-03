### [Why Did the Cow Cross the Road](http://usaco.org/index.php?page=viewproblem2&cpid=720)

#### Problem Statement

Given a set of cows on each side of the road, assuming we can rotate either side, find the minimum number of crossing pairs.
We define a pair of cows as crossing if `(A_i < A_j) != (B_i < B_j)`.

#### Intuition
Assume that we rotate only the left side. When we rotate the last cow to the top, we remove exactly `N - 1 - B_i` crossings and create exactly `B_i` new ones. That's because we know that the cow `i` crosses every cow below `B_i` right now, and will cross every cow above `B_i` once we move it to the top.

#### Solution
Thus, we iterate through N such rotations, keeping track of a running minimum. The number of crossing paths for an initial setup is a well-known problem, and can be solved with a BIT.

#### Common Mistakes
It's important to remember to rotate both sides. Rotating one side alone does not guarantee getting the minimum. This bug caused me a lot of headaches.

#### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/mincross.java)