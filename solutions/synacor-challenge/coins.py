from itertools import permutations

def solve(coins, func, target):
    return next(iter(filter(lambda p: func(*p) == target, permutations(coins))))

print(solve([2, 7, 3, 5, 9], lambda a, b, c, d, e: a + b*c**2 + d**3 -e, 399))
