import math

from solve import next_perm

def count_permutations(l):
    l = sorted(l)
    count = 1
    while next_perm(l):
        count += 1
    return count

def test_next_perm():
    for i in range(1, 10):
        assert count_permutations(list(range(i))) == math.factorial(i)
