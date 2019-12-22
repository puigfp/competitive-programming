For part 1, the naive algorithm works.

For part 2, we can start from the end and apply the transformations in a backward order: we want to know which card ends up in position 2020 and we can compute where that card was before we applied the last transformation, and iterate that process until we find the initial position of the card (before any transformation was applied) which is the card's number.

Here, the trick is to notice that all inverse transformations are affine: `pos := a * pos + b mod length` for some `a` and `b`

We can combine two affine transformations (`a1, b1` and `a2, b2`) into a single one:

`pos := a1 * a2 * pos + a1 * b2 + b1 mod length`

We start by combining all the inverse transformations of our input into a single one, which gives use the affine transformation equivalent to one shuffle.

We can combine this transformation with itself, and we get the affine transformation that is equivalent to `2` shuffles.

We can continue this process to compute the affine transformations equivalent to `2^n` shuffles for any `n`.

To find the answer, we compute the binary decomposition of `101741582076661`, which effectively decompose the `101741582076661` shuffles into a sequence of some of the transformations we computed. We merge those transformations into a single one to compute the affine transformation equivalent to `101741582076661` shuffles.

Combining the transformations also speeds up part 1.
