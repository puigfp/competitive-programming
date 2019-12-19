from random import randrange

from fenwick import Fenwick


def test_fenwick_edge():
    f = Fenwick([])
    assert f.sum(0) == 0

    f = Fenwick([1] * 10)
    assert f.sum(0) == 0
    assert f.sum(10) == 10


def test_fenwick_random():
    l = [randrange(-10, 10) for _ in range(139)]
    f = Fenwick(l)

    for _ in range(100):
        # random l update
        i = randrange(0, len(l))
        x = randrange(-100, 100)
        l[i] += x
        f.add(i, x)

        # check that the naive method and the fenwick tree agree
        assert all(
            sum(l[i:j]) == f.sum_range(i, j)
            for i in range(len(l) + 1)
            for j in range(i, len(l) + 1)
        )
