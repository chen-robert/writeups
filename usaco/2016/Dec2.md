### [Team Building](http://usaco.org/index.php?page=viewproblem2&cpid=673)

#### Problem Statement
>Every year, Farmer John brings his N cows to compete for "best in show" at the state fair. His arch-rival, Farmer Paul, brings his M cows to compete as well (1≤N≤1000,1≤M≤1000).
>Each of the N+M cows at the event receive an individual integer score. However, the final competition this year will be determined based on teams of K cows (1≤K≤10), as follows: Farmer John and Farmer Paul both select teams of K of their respective cows to compete. The cows on these two teams are then paired off: the highest-scoring cow on FJ's team is paired with the highest-scoring cow on FP's team, the second-highest-scoring cow on FJ's team is paired with the second-highest-scoring cow on FP's team, and so on. FJ wins if in each of these pairs, his cow has the higher score.
>Please help FJ count the number of different ways he and FP can choose their teams such that FJ will win the contest. That is, each distinct pair (set of K cows for FJ, set of K cows for FP) where FJ wins should be counted. Print your answer modulo 1,000,000,009.
#### Observations
This is a fairly trivial DP. Let `DP[n][m][k]` be the number of ways to pair off k cows, using up to n of John's cows and m of Paul's cows.

Observe `DP[n][m][k]` is equal to the summation of all `DP[i][j][k-1]` for `0 <= i < n` and `0 <= j < m`. For **O(1)** computation of this value, we can use lookup tables. Specifically, `lp[i][j] = lp[i-1][j] + lp[i][j-1] - lp[i-1][j-1] + DP[i][j]`.

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2016/code/team.java)