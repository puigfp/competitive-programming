from collections import deque, namedtuple

node = namedtuple("node", ["sum", "updates"])
update = namedtuple("update", ["x", "y", "value"])


def init_segment_tree(l):
    size = 1
    while size < len(l):
        size *= 2
    tree = (
        [node(0, deque())] * size
        + [node(elem, deque()) for elem in l]
        + [node(0, deque())] * (size - len(l))
    )

    for i in reversed(range(1, size)):
        tree[i] = node(tree[2 * i][0] + tree[2 * i + 1][0], deque())

    return tree


def query(x, y, tree):

    # rec(x0, y0, k):
    # returns the sum over the intersection of [x, y[ and [x0, y0[, assuming k is the
    # index associated with the [x0, y0[ segment
    def rec(x0, y0, k):
        if y0 <= x or y <= x0:
            return 0

        # make sure we are using up to date data by applying lazy updates
        apply_updates(x0, y0, k, tree)

        if x <= x0 <= y0 <= y:
            return tree[k].sum

        z0 = x0 + (y0 - x0) // 2
        return rec(x0, z0, 2 * k) + rec(z0, y0, 2 * k + 1)

    return rec(0, len(tree) // 2, 1)


def add_update(x, y, value, tree):
    tree[1].updates.append(update(x, y, value))


def apply_updates(x0, y0, k, tree):
    while tree[k][1]:

        u = tree[k][1].popleft()
        x, y, value = u

        # nothing to do:
        # [x, y[ and [x0, y0[ do not intersect
        if y0 <= x or y <= x0:
            continue

        # this node doesn't have children (base case)
        if y0 - x0 == 1:
            tree[k] = node(value, tree[k].updates)
            continue

        # this node has children -> push update down
        tree[2 * k].updates.append(u)
        tree[2 * k + 1].updates.append(u)

        # lazy case: we can update this node without actually updating its children
        if x <= x0 < y0 <= y:
            tree[k] = node((y0 - x0) * value, tree[k].updates)
            continue

        # usual case: we have to update the children to know this node's new value
        z0 = x0 + (y0 - x0) // 2
        apply_updates(x0, z0, 2 * k, tree)
        apply_updates(z0, y0, 2 * k + 1, tree)
        tree[k] = node(tree[2 * k].sum + tree[2 * k + 1].sum, tree[k].updates)


def read_segments():
    # reads problem input
    n = int(input())
    segments = list()
    for _ in range(n):
        xa, ha, xb, hb = map(int, input().split())
        segments.append(((xa, ha), (xb, hb)))
    return segments


def is_above(segment1, segment2):
    # returns True if segment1 is above segment2
    # assumes x1 <= x <= x2
    (x1, y1), (x2, y2) = segment1
    (x, y) = segment2[0]
    return (y2 - y1) / (x2 - x1) * (x - x1) + y1 >= y


def sort_segments(segments):
    # topologically sort segment (if segment1 is above segment2, then segment1 will be
    # before segment 2 in the sorted list)
    ids = sorted(range(len(segments)), key=lambda i: segments[i])
    adj = [[] for i in ids]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if segments[ids[i]][1][0] < segments[ids[j]][0][0]:
                break
            if is_above(segments[ids[i]], segments[ids[j]]):
                adj[ids[i]].append(ids[j])
            else:
                adj[ids[j]].append(ids[i])
    sort = topological_sort(adj)
    return sort


def topological_sort(adj):
    inbound_edges = {i: 0 for i in range(len(adj))}
    for i in range(len(adj)):
        for j in adj[i]:
            inbound_edges[j] += 1

    no_inbound_edges = deque([i for i, c in inbound_edges.items() if c == 0])
    sort = []

    while no_inbound_edges:
        i = no_inbound_edges.popleft()
        for j in adj[i]:
            inbound_edges[j] -= 1
            if inbound_edges[j] == 0:
                no_inbound_edges.append(j)
        sort.append(i)

    return sort


def solve(segments):
    x_max = max(max(elem[0][0], elem[1][0]) for elem in segments)
    tree = init_segment_tree([0, 1] * (x_max + 1))
    order = sort_segments(segments)
    water = dict()
    for i in order:
        (x1, y1), (x2, y2) = segments[i]
        s = query(x1 * 2, x2 * 2 + 1, tree)
        water[i] = s
        if y1 < y2:
            add_update(2 * x1, 2 * x1 + 1, s, tree)
            add_update(2 * x1 + 1, 2 * x2 + 1, 0, tree)
        else:
            add_update(2 * x2, 2 * x2 + 1, s, tree)
            add_update(2 * x1, 2 * x2, 0, tree)

    for i in sorted(water):
        print(water[i])


if __name__ == "__main__":
    segments = read_segments()
    solve(segments)
