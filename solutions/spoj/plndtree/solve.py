from collections import defaultdict, deque


def add_word(a, b):
    # a += b
    # a, b: dict(letter -> count)
    for letter, count in b.items():
        a[letter] = a.get(letter, 0) + count
        if a[letter] == 0:
            del a[letter]


def remove_word(a, b):
    # a -= b
    # a, b: dict(letter -> count)
    for letter, count in b.items():
        a[letter] = a.get(letter, 0) - count
        if a[letter] == 0:
            del a[letter]


class Fenwick:
    def __init__(self, l):
        self.l = [dict() for _ in range(len(l) + 1)]
        for i, x in enumerate(l):
            self.add(i, x)

    def add(self, i, x):
        # l[i] += x
        assert 0 <= i < len(self.l) - 1
        i += 1
        while i < len(self.l):
            add_word(self.l[i], x)
            i += i & -i

    def sum(self, i):
        # sum(l[:i])
        assert 0 <= i < len(self.l)
        s = dict()
        while i > 0:
            add_word(s, self.l[i])
            i -= i & -i
        return s

    def sum_range(self, i, j):
        # sum(l[i:j])
        assert 0 <= i <= j < len(self.l)
        a = self.sum(j)
        b = self.sum(i)
        remove_word(a, b)
        return a


def flatten_tree(adj):
    q = deque([1])

    beg = dict()
    end = dict()

    i = 0
    while q:
        current = q.pop()

        if current not in beg:
            beg[current] = i
            i += 1

            q.append(current)
            for neighbor in adj[current]:
                if neighbor not in beg:
                    q.append(neighbor)

        end[current] = i

    return beg, end


if __name__ == "__main__":
    N = int(input())

    # read adjacency matrix
    adj = defaultdict(list)
    for _ in range(N - 1):
        x, y = map(int, input().split())
        adj[x].append(y)
        adj[y].append(x)

    # debug purposes
    for l in adj.values():
        l.sort(reverse=True)

    # "flatten" tree
    beg, end = flatten_tree(adj)

    # init fenwick tree
    letters = input()
    assert len(letters) == N
    l = [None] * N
    for i, letter in zip(range(1, N + 1), letters):
        l[beg[i]] = {letter: 1}
    tree = Fenwick(l)

    M = int(input())
    for _ in range(M):
        line = [s for s in input().split()]

        # update tree
        if line[0] == "0":
            i = int(line[1])
            new_char = line[2]

            # retrieve current char from tree
            current_value = tree.sum_range(beg[i], beg[i] + 1)
            assert len(current_value) == 1
            prev_char = next(iter(current_value.keys()))

            # no-op update edge case handling
            if new_char != prev_char:
                tree.add(beg[i], {new_char: 1, prev_char: -1})

        # palindrome check
        if line[0] == "1":
            i = int(line[1])
            letters = tree.sum_range(beg[i], end[i])
            evens = sum(1 for count in letters.values() if count % 2 == 1)
            print("YES" if evens in [0, 1] else "NO")
