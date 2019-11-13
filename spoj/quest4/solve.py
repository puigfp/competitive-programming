def max_bipartite_matching(bigraph):
    matching = [None] * len(bigraph)
    for i in range(len(bigraph)):
        augment_bipartite_matching(bigraph, i, matching)
    return matching


def augment_bipartite_matching(bigraph, start, matching):
    visit = [False] * len(bigraph)

    def dfs(left_node):
        for right_node in bigraph[left_node]:

            if visit[right_node]:
                continue
            visit[right_node] = True

            if matching[right_node] is None or dfs(matching[right_node]):
                matching[right_node] = left_node
                return True

        return False

    return dfs(start)

def solve(tiles):
    bigraph = [[] for _ in range(120)]
    for (x, y) in tiles:
        bigraph[x].append(y)

    matching = max_bipartite_matching(bigraph)
    return len([x for x in matching if x is not None])

if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        N = int(input())
        tiles = [tuple(map(int, input().split())) for _ in range(N)]
        print(solve(tiles))
