### [262144](http://usaco.org/index.php?page=viewproblem2&cpid=648)

#### Problem Statement
> She is particularly intrigued by the current game she is playing. The game starts with a sequence of N positive integers (2≤N≤262,144), each in the range 1…40. In one move, Bessie can take two adjacent numbers with equal values and replace them a single number of value one greater (e.g., she might replace two adjacent 7s with an 8). The goal is to maximize the value of the largest number present in the sequence at the end of the game. Please help Bessie score as highly as possible!

#### Solution
First considering combining all of the ones. If a segment has an even number of ones, it can be fully condensed down into twos. Otherwise, we'll end up breaking up our sequence into two distinct parts. That's because the leftover one will never be able to be removed. 

We use a greedy solution. Having a bigger sequence will always produce the same or a bigger number than a smaller one. With this in mind, we divide our original big sequence up into many smaller sequences. When doing so, we seek to maximize the number of twos appended for each subsequence. In particular, if a sequence is bordered by N ones (where N is odd), we add `floor(N / 2)` twos to the new sequence.

Applying similar logic to 2, 3, 4, and so on, we solve the problem.

Note that because the numbers are limited to a very small range, this doesn't exceed runtime. 
##### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/_262144.java)