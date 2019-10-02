### [Why Did the Cow Cross the Road II](http://usaco.org/index.php?page=viewproblem2&cpid=721)

#### Solution
This is a classic RMQ problem. For every cow, we maintain a running maximum of the number of crosswalks that can be drawn, using the cows from `0 to j`. Note that only `8 * N` updates ever occur because every cow has a maximum of 8 other cows they can draw a crosswalk to.
#### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/maxflow.java)