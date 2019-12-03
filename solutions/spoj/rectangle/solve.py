import functools
from collections import defaultdict

lower, upper = int(input()), int(input())

factorizations = defaultdict(list)
for i in range(lower, upper+1):
    for j in range(i, upper+1):
        factorizations[i*j].append((i, j))

@functools.lru_cache(maxsize=None)
def p1(perimeter):
    for width in range(
        max(perimeter - upper, lower),
        min(perimeter - lower, upper, perimeter // 2) + 1,
    ):
        height = perimeter - width
        if len(factorizations[width * height]) == 1:
            return False
    return True

@functools.lru_cache(maxsize=None)
def p2(area):
    candidate = None
    for (width, height) in factorizations[area]:
        if p1(width + height):
            if candidate is not None:
                return None
            candidate = (width, height)
    return candidate

@functools.lru_cache(maxsize=None)
def p3(perimeter):
    candidate = None
    for width in range(
        max(perimeter - upper, lower),
        min(perimeter - lower, upper, perimeter // 2) + 1,
    ):
        height = perimeter - width
        if (width, height) == p2(width * height):
            if candidate is not None:
                return None
            candidate = (width, height)
    return candidate

def solve():
    l = []
    for perimeter in range(2*lower, 2*upper + 1):
        c = p3(perimeter)
        if c is not None:
            l.append(c)
    l.sort()
    return l

for (a, b) in solve():
    print(a, b)

# without this, if the program didn't output anything, the test doesn't pass on SPOJ
print()
