### [Lots of Triangles](http://usaco.org/index.php?page=viewproblem2&cpid=672)

#### Problem Statement
>Farmer John is thinking of selling some of his land to earn a bit of extra income. His property contains n trees (3≤N≤300), each described by a point in the 2D plane, no three of which are collinear. FJ is thinking about selling triangular lots of land defined by having trees at their vertices;
>A triangular lot has value v if it contains exactly v trees in its interior (the trees on the corners do not count, and note that there are no trees on the boundaries since no three trees are collinear). For every v=0…N−3, please help FJ determine how many of his L potential lots have value v.

#### Observations
For all pairs of trees, we store the number of trees under this line. Because no three trees are collinear, none will overlap with this line. This takes O(N^3) time. 

Observe that by doing this, we can find the number of trees within an arbitrary triangle. We do this by adding or subtracting the number of trees under each edge.

#### Solution
More specifically, we add the value if the edge is above last remaining point in the triangle, and we subtract it if it is below. 

Doing this for O(N^3) triangles finishes. 

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2016/code/triangles.java)