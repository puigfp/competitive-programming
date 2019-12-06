from collections import deque
import functools


def lines_to_graph_part1(lines):
    graph = dict()
    for line in lines:
        a, b = line.strip().split(")")
        graph[a] = graph.get(a, [])
        graph[b] = graph.get(b, [])
        graph[b].append(a)
    return graph


def solve_part1(graph):
    @functools.lru_cache(maxsize=None)
    def count_children(node):
        return len(graph[node]) + sum(count_children(child) for child in graph[node])

    return sum(count_children(node) for node in graph)


def lines_to_graph_part2(lines):
    graph = dict()
    for line in lines:
        a, b = line.strip().split(")")
        graph[a] = graph.get(a, [])
        graph[b] = graph.get(b, [])
        graph[b].append(a)
        graph[a].append(b)
    return graph


def solve_part2(graph):
    q = deque([("YOU", 0)])
    seen = {"YOU"}
    while q:
        node, l = q.popleft()
        for neighbor in graph[node]:
            if neighbor == "SAN":
                return l - 1
            elif neighbor not in seen:
                seen.add(neighbor)
                q.append((neighbor, l + 1))


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()

    print(f"Part 1: {solve_part1(lines_to_graph_part1(lines))}")
    print(f"Part 2: {solve_part2(lines_to_graph_part2(lines))}")
