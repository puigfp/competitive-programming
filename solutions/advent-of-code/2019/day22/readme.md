For part 1, the naive algorithm works.

For part 2, we can start from the end and apply the transformations in a backward order: we want to know which card ends up in position 2020 and we can compute where that card was before we applied the last transformation, and iterate that process until we find the initial position of the card (before any transformation was applied) which is the card's number.

Here, the trick is to notice that all the transformations are affine:

$$
x_{n+1} = a_1 x_n + b_1 \text{ mod } p
$$

We can combine two affine transformations ($(a_1, b_1)$ and $(a_2, b_2)$) into a single one:

$$
x_{n+2} = a_1 a_2 x_n + a_1 b_2 + b_1 \text{ mod } p
$$

We can also inverse any affine transformation:

$$
y = ax + b \text{ mod } p \iff x = a^{-1} y - a^{-1} b \text{ mod } p
$$

We start by combining all the transformations of our input into a single one, which gives use the affine transformation equivalent to one shuffle. Then, we inverse than transformation.

We can combine this transformation with itself, and we get the affine transformation that is equivalent to $2$ inverse shuffles.

We can continue this process to compute the affine transformations equivalent to $2^n$ inverse shuffles for any $n$.

To find the answer, we compute the binary decomposition of $101741582076661$, which effectively decompose the $101741582076661$ inverse shuffles into a sequence of some of the transformations we computed. We merge those transformations into a single one to compute the affine transformation equivalent to $101741582076661$ shuffles.

Combining the transformations also speeds up part 1.
