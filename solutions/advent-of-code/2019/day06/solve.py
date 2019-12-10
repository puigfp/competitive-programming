from collections import deque, defaultdict


def lines_to_graph_part1(lines):
    graph = defaultdict(lambda: [])
    for line in lines:
        a, b = line.strip().split(")")
        graph[a].append(b)
    return graph


def solve_part1(graph):
    q = deque([("COM", 0)])
    total_parents = 0

    while q:
        node, parents = q.popleft()
        total_parents += parents
        for child in graph[node]:
            q.append((child, parents + 1))

    return total_parents


def lines_to_graph_part2(lines):
    graph = defaultdict(lambda: [])
    for line in lines:
        a, b = line.strip().split(")")
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
