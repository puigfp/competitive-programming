---
link: https://open.kattis.com/problems/ballsandneedles
---

Problem originally from ACM SWERC 2016.

DFS:
- one DFS per connected component
- each DFS must visit every edge exactly once
- if we a node gets enqueued 2 times, it means we found 2 different paths from the starting node to this node, ie, we found a cycle in the graph
