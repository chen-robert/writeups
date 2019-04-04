### [High Card Low Card (Platinum)](http://usaco.org/index.php?page=viewproblem2&cpid=577)

#### Problem Statement
> Bessie and her friend Elsie are currently playing a simple card game where they take a deck of 2N cards, conveniently numbered 1…2N, and divide them into N cards for Bessie and N cards for Elsie. The two then play N rounds, where in each round Bessie and Elsie both play a single card. Initially, the player who plays the highest card earns a point. However, at one point during the game, Bessie can decide to switch the rules so that for the rest of the game, the player who plays the lowest card wins a point. Bessie can choose not to use this option, leaving the entire game in "high card wins" mode, or she can even invoke the option right away, making the entire game follow the "low card wins" rule.

In other words....

#### Sample
**Input**
```
4
1
8
4
3
```
**Output**
```3```
>Here, Bessie must have cards 2, 5, and 6, and 7 in her hand, and she can use these to win at most 3 points. For example, she can defeat the 1 card and then switch the rules to "low card wins", after which she can win two more rounds.
#### Solution
Consider the case where Bessie never switches the rules. We can approach this with a greedy solution. Every time, Bessie either plays the lowest card that can beat Elsie's card, or her lowest card if none of her cards are greater than Elsie's card. This works because we want to maximize the number of points, and each card can only be used to get at most one point. That means, if there is an opportunity to win a point with our card, we should take it.

Maintain a lookup for each index, where we store the maximum number of points we can win from the cards with index 1 to N. 

Now, do the same thing but in reverse. Assume Bessie changes the rules immediately, and now work from right to left. Similarly, store the values in a suffix table.

We assert that we can combine the two tables to get the best answer.
> e.g. `max([prefix[i] + suffix[i+1] for i in range(N)])`

The only problem that we may encounter is that there will be duplicates. For example, we both the suffix and prefix sum calculations use the same card. However, this can be alleviated easily. If there is a duplicate, there must also be an unused card. If this unused card is greater than the duplicate card, we can replace the duplicate card used in the suffix table with our unused card. Similar reasoning applies for the prefix table. That means, duplicates don't matter. 

#### Code

My solution can be found [here](https://github.com/chen-robert/writeups/blob/master/usaco/2015/code/_262144.java)