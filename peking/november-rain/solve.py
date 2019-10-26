from collections import deque, namedtuple

node = namedtuple("node", ["sum", "updates"])
update = namedtuple("update", ["x", "y", "value"])


def init_segment_tree(n):
    size = 1
    while size < n:
        size *= 2
    tree = [node(0, deque())] * size + [
        node(1, deque()) if i < n else node(0, deque()) for i in range(size)
    ]

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

def test_segment_tree():
    tree = init_segment_tree(6)
    assert 3 == query(0, 3, tree)
    assert 6 == query(0, 8, tree)
    assert 0 == query(6, 8, tree)

    add_update(0, 6, 2, tree)
    assert 6 == query(0, 3, tree)
    assert 12 == query(0, 8, tree)

    add_update(0, 8, 0, tree)
    add_update(0, 2, 10, tree)
    add_update(4, 6, -12, tree)
    add_update(0, 6, 1, tree)
    add_update(0, 1, 3, tree)
    add_update(2, 6, -1, tree)
    assert 3 == query(0, 3, tree)
    assert 0 == query(0, 6, tree)
    assert 1 == query(1, 2, tree)
