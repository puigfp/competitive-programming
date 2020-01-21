from collections import defaultdict
import sys


def edge_to_adj(edges):
    adj = defaultdict(set)
    for node1, node2 in edges:
        if node1 != node2:
            adj[node1].add(node2)
            adj[node2].add(node1)
    return adj


def cycle_detection(adj):
    adj = {key: set(neighbors) for key, neighbors in adj.items()}

    seen = set()

    def dfs(start):
        q = [start]
        while q:
            node = q.pop()
            if node in seen:  # we found a cycle !
                return True
            seen.add(node)
            for neighbor in adj[node].copy():
                # enqueue neighbor and remove visited edge from adj
                adj[node].remove(neighbor)
                adj[neighbor].remove(node)
                q.append(neighbor)
        return False

    for node in adj:
        if node not in seen and dfs(node):
            return True

    return False


if __name__ == "__main__":
    stdin_iter = iter(sys.stdin)
    while True:
        # XXX: the problem statement doesn't provide any information about a stop token
        try:
            N = int(next(stdin_iter))
        except StopIteration:
            break
        edges3d = []
        for _ in range(N):
            x0, y0, z0, x1, y1, z1 = map(int, next(stdin_iter).split())
            edges3d.append(((x0, y0, z0), (x1, y1, z1)))
        edges2d = [(node1[:2], node2[:2]) for node1, node2 in edges3d]
        print(
            "True closed chains"
            if cycle_detection(edge_to_adj(edges3d))
            else "No true closed chains"
        )
        print(
            "Floor closed chains"
            if cycle_detection(edge_to_adj(edges2d))
            else "No floor closed chains"
        )
