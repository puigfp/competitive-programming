---
link: https://onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1260
---

Quick notes:

- the problem can be reduced to the 2SAT problem:

    if the traffic directions are correctly set, then, for a given route, if the traffic directions aren't right for one of the direct path, they must be right for the other one

- we don't need to solve 2SAT, but only to check that it's solvable

- to do that we only check that, for every x, we don't have (not x => x) and (x => not x) (ie, that x and not x are not in the same strongly connected component)
