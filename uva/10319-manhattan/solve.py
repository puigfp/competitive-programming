from collections import defaultdict

STREET, AVENUE = 0, 1


def solve(routes):
    clauses = routes_to_2sat(routes)
    return is_2sat_solvable(clauses)

def route_to_2sat(route):
    ((a, b), (c, d)) = route

    if b < d:
        s_a = (True, (STREET, a))
        s_c = (True, (STREET, c))
    elif b > d:
        s_a = (False, (STREET, a))
        s_c = (False, (STREET, c))

    if a < c:
        a_b = (True, (AVENUE, b))
        a_d = (True, (AVENUE, d))
    elif a > c:
        a_b = (False, (AVENUE, b))
        a_d = (False, (AVENUE, d))

    if b == d:
        return [(a_b, a_b)]

    if a == c:
        return [(s_a, s_a)]

    return [
        (s_a, s_c),
        (a_b, a_d),
        (s_a, a_b),
        (s_c, a_d),
    ]


def routes_to_2sat(routes):
    return [
        e
        for route in routes
        for e in route_to_2sat(route)
    ]

def path_adj(adj, c1, c2):
    seen = set()

    def dfs(a):
        if a == c2:
            return True

        if a in seen:
            return

        seen.add(a)

        for b in adj[a]:
            if dfs(b):
                return True

        return False

    return dfs(c1)

def is_2sat_solvable(clauses):
    adj = defaultdict(set) # adjacency matrix
    for (c1, c2) in clauses:
        adj[(not c1[0], c1[1])].add(c2)
        adj[(not c2[0], c2[1])].add(c1)
        # create sets to make sure the dict's size doesn't change in the future
        adj[c1], adj[c2]

    for c1 in adj:
        # If there are paths:
        # - from c1 to not c1
        # - from not c1 to c1
        # Then this instance of 2SAT isn't solvable.
        if path_adj(adj, (not c1[0], c1[1]), c1) and \
            path_adj(adj, c1, (not c1[0], c1[1])):
            return False

    return True

if __name__ == "__main__":
    N = int(input())
    for _ in range(N):
        _, _, n = list(map(int, input().split()))
        routes = list()
        for _ in range(n):
            a, b, c, d = map(int, input().split())
            routes.append(((a, b), (c, d)))
        print("Yes" if solve(routes) else "No")
