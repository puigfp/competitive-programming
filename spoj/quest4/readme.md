---
link: https://www.spoj.com/problems/QUEST4/
---

Finding a way of using the planks to cover the grids is equivalent to finding the [vertex cover](https://en.wikipedia.org/wiki/Vertex_cover) of a bipartite graph:

- left nodes are the lines of the room
- right nodes are the columns of the room
- edges are all the (i, j) that are grid locations

We want to find the smallest set of vertexes such as any edge of the graph is incident to at least one vertex of this set.

The size of this set is the size of the maximum bipartite matching of this graph, according to [Kőnig's theorem](https://en.wikipedia.org/wiki/K%C5%91nig%27s_theorem_(graph_theory)).
