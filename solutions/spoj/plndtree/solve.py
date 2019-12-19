from collections import defaultdict, deque


def letter_to_word(letter):
    return 1 << ord(letter) - ord("a")


def plus_words(a, b):
    return a ^ b


def is_palindrome(a):
    return a == 0 or a - (a & -a) == 0


class Fenwick:
    def __init__(self, l):
        self.l = [0 for _ in range(len(l) + 1)]
        for i, x in enumerate(l):
            self.add(i, x)

    def add(self, i, x):
        # l[i] += x
        assert 0 <= i < len(self.l) - 1
        i += 1
        while i < len(self.l):
            self.l[i] = plus_words(self.l[i], x)
            i += i & -i

    def sum(self, i):
        # sum(l[:i])
        assert 0 <= i < len(self.l)
        s = 0
        while i > 0:
            s = plus_words(s, self.l[i])
            i -= i & -i
        return s

    def sum_range(self, i, j):
        # sum(l[i:j])
        assert 0 <= i <= j < len(self.l)
        a = self.sum(j)
        b = self.sum(i)
        return plus_words(a, b)


def flatten_tree(adj):
    q = deque([0])

    beg = [None] * len(adj)
    end = [None] * len(adj)

    i = 0
    while q:
        current = q.pop()

        if beg[current] is None:
            beg[current] = i
            i += 1

            q.append(current)
            for neighbor in adj[current]:
                if beg[neighbor] is None:
                    q.append(neighbor)

        end[current] = i

    return beg, end


if __name__ == "__main__":
    N = int(input())

    # read adjacency matrix
    adj = [[] for _ in range(N)]
    for _ in range(N - 1):
        x, y = map(int, input().split())
        adj[x - 1].append(y - 1)
        adj[y - 1].append(x - 1)

    # debug purposes
    for l in adj:
        l.sort(reverse=True)

    # "flatten" tree
    beg, end = flatten_tree(adj)

    # init fenwick tree
    letters = input()
    assert len(letters) == N
    l = [None] * N
    for i, letter in enumerate(letters):
        l[beg[i]] = letter_to_word(letter)
    tree = Fenwick(l)

    M = int(input())
    for _ in range(M):
        line = [s for s in input().split()]

        # update tree
        if line[0] == "0":
            i = int(line[1]) - 1

            new_char = letter_to_word(line[2])
            prev_char = tree.sum_range(beg[i], beg[i] + 1)

            # no-op update edge case handling
            if new_char != prev_char:
                tree.add(beg[i], plus_words(new_char, prev_char))

        # palindrome check
        if line[0] == "1":
            i = int(line[1]) - 1
            letters = tree.sum_range(beg[i], end[i])
            print("YES" if is_palindrome(letters) else "NO")

