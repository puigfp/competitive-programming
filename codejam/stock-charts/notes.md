---
link: https://code.google.com/codejam/contest/204113/dashboard#s=p2
---

Let G be the graph of charts: there is a directed edge from A to B if chart A can be drawn below chart B.

Any path in that graph represents a set of charts that can be drawn on a single chart without them overlapping. What we want to find is the smallest number of disjoint paths required to cover all the nodes of the graph.

The [judge notes](https://code.google.com/codejam/contest/204113/dashboard#s=a&a=2) explain how finding the smallest number of paths can be reduced to finding a maximum bipartite matching (in another graph, not G).
