import heapq

def topological_sort(adj):
    inbound_edges = [0 for _ in adj]
    for l in adj:
        for i in l:
            inbound_edges[i] += 1

    q = [i for i in range(len(inbound_edges)) if inbound_edges[i] == 0]
    heapq.heapify(q)

    sort = []
    while q:
        next_task = heapq.heappop(q)
        sort.append(next_task)
        for i in adj[next_task]:
            inbound_edges[i] -= 1
            if inbound_edges[i] == 0:
                heapq.heappush(q, i)

    return sort

if __name__ == "__main__":
    N, M = map(int, input().split())
    adj = [[] for _ in range(N)]
    for _ in range(M):
        l = [int(i) - 1 for i in input().split()]
        i = l[0]
        for j in l[2:]:
            adj[j].append(i)
    print(" ".join(str(i + 1) for i in topological_sort(adj)))
