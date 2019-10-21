from collections import namedtuple

node = namedtuple("node", ["max", "max_suffix", "max_prefix", "sum"])

def build_tree(numbers):
    size = 1
    while size < len(numbers):
        size *= 2
    numbers = numbers + [0] * (size - len(numbers))
    tree = [0] * size + [node(e, e, e, e) for e in numbers]

    def build(x, y, k):
        if y - x == 1:
            return tree[k]

        left_value = build(x, x + (y - x) // 2, 2 * k)
        right_value = build(x + (y - x) // 2, y, 2 * k + 1)

        max_ = max(
            left_value.max_suffix + right_value.max_prefix,
            left_value.max,
            right_value.max,
        )

        max_prefix = max(
            left_value.max_prefix,
            left_value.sum + right_value.max_prefix,
        )

        max_suffix = max(
            right_value.max_suffix,
            left_value.max_suffix + right_value.sum,
        )

        tree[k] = node(
            max_,
            max_suffix,
            max_prefix,
            left_value.sum + right_value.sum,
        )

        return tree[k]

    build(0, size, 1)
    return tree

def query(x, y, tree):

    def rec(x0, y0, k):
        """
        return max sum from i to j
            where max(x, x0) <= i <= j <= min(y, y0)
        """

        if x <= x0 <= y0 <= y:
            return tree[k]

        z0 = x0 + (y0 - x0) // 2
        if y <= z0:
            return rec(x0, z0, 2 * k)
        if x >= z0:
            return rec(z0, y0, 2 * k + 1)

        left_value = rec(x0, z0, 2 * k)
        right_value = rec(z0, y0, 2 * k + 1)

        max_ = max(
            left_value.max_suffix + right_value.max_prefix,
            left_value.max,
            right_value.max,
        )

        max_prefix = max(
            left_value.max_prefix,
            left_value.sum + right_value.max_prefix,
        )

        max_suffix = max(
            right_value.max_suffix,
            left_value.max_suffix + right_value.sum,
        )

        return node(
            max_,
            max_suffix,
            max_prefix,
            left_value.sum + right_value.sum,
        )

    return rec(0, len(tree) // 2, 1)

n = int(input())
numbers = list(map(int, input().split()))
tree = build_tree(numbers)

m = int(input())
for _ in range(m):
    x, y = map(int, input().split())
    print(query(x - 1, y, tree).max)

