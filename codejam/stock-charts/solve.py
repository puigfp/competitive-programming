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


def charts_to_bipartite_graph(charts):
    return [
        [
            right
            for right, right_chart in enumerate(charts)
            # if left_chart < right_chart
            if all(e1 < e2 for (e1, e2) in zip(left_chart, right_chart))
        ]
        for left_chart in charts
    ]


cases = int(input())
for i in range(cases):
    n, _ = map(int, input().split())
    charts = [list(map(int, input().split())) for _ in range(n)]
    bigraph = charts_to_bipartite_graph(charts)
    matching = max_bipartite_matching(bigraph)
    matching_size = len(matching) - matching.count(None)
    print(f"Case #{i+1}: {len(charts) - matching_size}")
