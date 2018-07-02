### [Max Flow](http://usaco.org/index.php?page=viewproblem2&cpid=576)

##### Problem Statement
> Farmer John has installed a new system of N−1 pipes to transport milk between the N stalls in his barn **(2≤N≤50,000)**, conveniently numbered 1…N. Each pipe connects a pair of stalls, and all stalls are connected to each-other via paths of pipes.
> FJ is pumping milk between K pairs of stalls **(1≤K≤100,000)**. For the ith such pair, you are told two stalls si and ti, endpoints of a path along which milk is being pumped at a unit rate. Please help him determine the maximum amount of milk being pumped through any stall. If milk is being pumped along a path from **u** to **v**, then it counts as being pumped through the endpoint stalls **u** and **v**, as well as through every stall along the path between them

In other words, we're given a tree and a series of paths on that tree. We need to find the point at which the most paths intersect. 

Observe the trivial case in which the tree is actually a linked list. We could increment a counter at the start of every path, and decrement a counter at the end. 

Afterwards, run through the list maintaining a running count of the paths. 

In order to apply this to a tree, first arbitrarily root the tree. Observe that for every node, there's a unique path to the tree. 

Define the LCA (Least Common Ancestor) of two nodes to be the node that's furthest from the root, yet still is a ancestor to both nodes. For example, the LCA of nodes **5** and **6** is **1**. Similarly, the LCA of nodes **6** and **7** is **3**. 

![](https://www.geeksforgeeks.org/wp-content/uploads/lca.png)

Let **p(u)** be the path from node **u** to the root. Note that the path from **u -> v** is equal to `p(u) + p(v) - p(lca(u))`

We can use the preceding method to increment counters, extending our solution from a linked list to a tree. 

##### Tarjan's LCA
However, we still need an efficient way to calculate the LCA of two nodes. Note that our queries are offline (we don't need to process them in order). 

![](https://www.geeksforgeeks.org/wp-content/uploads/tre22.png)


To understand why this works, consider nodes **u** and **v**. There are two cases when finding LCA. 
> 1. **u** is a child of **v** or vice versa. This LCA for this case is trivial (it's u or v). 
> 2. Let the LCA of the two nodes be **t**. **u** and **v** are on separate child branches of **t**. After visiting **u** the program will back track to **t** and make the ancestor of **u**, **t**. Once the program visits **v**, it'll find that **u** is black (has been visited), and print out the LCA.  

##### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/maxflow.java)