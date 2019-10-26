def init_segment_tree(n):
    size = 1
    while size < n:
        size *= 2
    tree = [0] * size + [1 if i < n else 0 for i in range(size)]

    for i in reversed(range(1, size)):
        tree[i] = tree[2*i] + tree[2*i+1]

    return tree

def query(x, y, tree):

    def rec(x0, y0, k):
        if x <= x0 <= y0 <= y:
            return tree[k]

        z0 = x0 + (y0 - x0) // 2
        if y <= z0:
            return rec(x0, z0, 2 * k)
        if x >= z0:
            return rec(z0, y0, 2 * k + 1)

        left_value = rec(x0, z0, 2 * k)
        right_value = rec(z0, y0, 2 * k + 1)

        return left_value + right_value

    return rec(0, len(tree) // 2, 1)

def update(x, y, value, tree):

    def rec(x0, y0, k):
        if y0 - x0 == 1:
            tree[k] = value
            return

        z0 = x0 + (y0 - x0) // 2
        if y <= z0:
            rec(x0, z0, 2 * k)
        elif x >= z0:
            rec(z0, y0, 2 * k + 1)
        else:
            rec(x0, z0, 2 * k)
            rec(z0, y0, 2 * k + 1)

        tree[k] = tree[2*k] + tree[2*k+1]

    return rec(0, len(tree) // 2, 1)


tree = init_segment_tree(6)
update(0, 2, 2, tree)
print(query(0, 3, tree))
print(tree)
