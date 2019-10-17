---
link: https://www.spoj.com/problems/RECTANGLE/
---

The extra test cases were taken from https://github.com/lucidsoftware/lucid-programming-competition-2018/tree/master/problems/rectangle/tests

Let $L \leq U$, $A = wh$ and $P=a+h$.

Avery knows $A$ and Pat knows $P$.

Let's write down what the discussion between Avery and Pat means:

- *Avery*: I don't know what $w$ and $h$ are.

  $\mathcal{P_0}(A)$: There are multiple ways (at least $2$) to factorize $A$ using only factors from $[L, U]$.

  

- *Pat*: I knew that.

  $\mathcal{P_1}(P)$: $\forall L \leq w \leq h \leq U$, $w + h = P \implies \mathcal{P_0}(wh)$ is true.

  

- *Avery*: Now I know what they are.

  $\mathcal{P_2}(A)$: $\exists ! L \leq w \leq h \leq U$, $A = wh$ and $\mathcal{P_1}(w+h)$ is true.

  If $\mathcal{P_2}(A)$ is true, let's call $(w, h) = f_2(A)$ the unique values for $w$ and $h$.

  

- *Pat*: I know too.

  $\mathcal{P_3}(P)$: $\exists ! L \leq w \leq h \leq U$, $w + h = P$, $\mathcal{P_2}(wh)$ is true and $(w, h) = f_2(wh)$

  If $\mathcal{P_3}(A)$ is true, let's call $(w, h) = f_3(P)$ the unique values for $w$ and $h$.



The idea of the algorithm is to implement those propositions in Python and then do a naive for loop to find all the $P \in [2L, 2U]$ for which $\mathcal{P_3}(P)$ is true (and the associated values for $(w, h) = f_3(P)$).

We heavily rely on memoization to avoid recomputing the same values multiple times. We calculating the complexity, we consider that each function runs exactly once for every possible input.

*Trick*: Two steps require to perform factorization (computing $\mathcal{P_0}(A)$ and $\mathcal{P_2}(A)$). We compute the factorizations for all possibles values of $A$ at the beginning of the algorithm (cost: $O(U^2)$) to make factorization a $O(1)$ operation.

The full complexity of this method is $O(U^2)$ (which is ok considering that $U \leq 1000$).

Useful:

- we have

  - $L \leq w \leq h \leq U$ 
  - $w + h = P$

- we can show

  - $w \leq P/2$
  - $P - U \leq w \leq h \leq P - L$

  (those inequalities are useful and used to compute some ranges in the code)