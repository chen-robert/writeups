### [Promotion Counting](http://usaco.org/index.php?page=viewproblem2&cpid=696)

#### Problem Statement
Given a tree, for each node find the number of its children who's value is greater than the original node's value.

#### Intuition
If we iterate over the nodes with a DFS, we guarantee that we'll visit all of the node's children. Furthermore, we can guarantee that between entering and exiting a node, the only nodes processed are that node's children.

More specifically, we maintain a BIT to keep track of our state. When we first visit a node, we sum from `i - N`. Then, we visit all of the node's children. After visiting all of the children recursively, we again compute the sum of `i - N`. The difference is our answer. Finally, we update the BIT with our current node's value and return.

#### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/maxflow.java)