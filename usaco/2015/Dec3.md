### [Counting Haybales](http://usaco.org/index.php?page=viewproblem2&cpid=578)

##### Problem Statement
>FJ's farm consists of N fields in a row, conveniently numbered 1…N. In each field there can be any number of haybales. Farmer John's instructions contain three types of entries: 
>
> 1) Given a contiguous interval of fields, add a new haybale to each field.
> 2) Given a contiguous interval of fields, determine the minimum number of haybales in a field within that interval.
> 3) Given a contiguous interval of fields, count the total number of haybales inside that interval.

From these three requirements, we know the problem probably requires implementing a data structure. Specifically, such a data structure must support **O(log N)** range updates, range sums, and range minimum queries. 

##### Lazy RMQ

In order to support range operations, we need to augment the traditional segment tree. 

The rationale behind our solution is that we want to postpone updates as much as possible. Due to the nature of a segment tree, we can often apply updates to an entire range at a time. We only need to resolve these updates when we're actually querying inside the range. 

For example, consider the node with value **9**. It spans the range 0 to 2. If we wanted to make a range update from say, 0 to 3, we would only need to update nodes **9** and **7**. Node **9** covers (0, 2) and node **7** covers (3, 3) (these values are inclusive). 

![](https://www.geeksforgeeks.org/wp-content/uploads/segment-tree1.png)

In pseudocode, our update function is

> Update range(left, right, delta):
> 1. If our current interval is completely inside **(left, right)**, change our node's pending update counter by **delta**
> 2. If our current node has pending updates, apply it, and pass on these updates downwards to its child nodes.
> 3. If our current interval is overlaps with but is not inside **(left, right)**, recursively call update on the child nodes. Then recalculate our current node's value. 

A Java implementation is as follows

```java
  /**
   * @param idx  Index
   * @param il  Left bound of interval at idx
   * @param ir  Right bound of interval at idx
   * @param delta  Amount to update each element in (ul, ur) by
   * @param ul  Left bound of update interval
   * @param ur  Right bound of update interval
   */
   void update(int idx, int il, int ir, int delta, int ul, int ur) {
    // If completely contained, change current update counter
    if (ul <= il && ir <= ur) {
      updates[idx] += delta;
    }

    processLazy(idx);

    if (il > ur || ir < ul || (ul <= il && ir <= ur)) {
      return;
    }

    // Recursively called upon child nodes
    int mid = (il + ir) / 2;
    update(l(idx), il, mid, delta, ul, ur);
    update(r(idx), mid + 1, ir, delta, ul, ur);

    // Recalculate current node
    recalc(idx);
  }
  void processLazy(int idx) {
    if (updates[idx] != 0) {
      // Apply pending update
      tree[idx] += updates[idx];

      // Pass pending update downwards to child nodes
      if (valid(l(idx))) updates[l(idx)] += updates[idx];
      if (valid(r(idx))) updates[r(idx)] += updates[idx];

      // Reset the update amount
      updates[idx] = 0;
    }
  }
```

##### Range Sums
Similarly, this technique can be applied to a Segment Tree for range sums. That implementation is left as an exercise to the reader. 

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/haybales.java)