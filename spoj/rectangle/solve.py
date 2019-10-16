import functools

primes = [2]
primes_until = 2

def generate_primes_until(n):
    global primes, primes_until
    for i in range(primes_until, n + 1):
        if all(i % prime != 0 for prime in primes):
            primes.append(i)
        primes_until = i

@functools.lru_cache(maxsize=None)
def is_prime(n):
    global primes
    generate_primes_until(n)
    return n in primes

@functools.lru_cache(maxsize=None)
def factorize(n):
    if n == 1 or is_prime(n):
        return [(1, n)]
    s = set()
    for prime in primes:
        if n % prime == 0:
            for (a, b) in factorize(n // prime):
                s.add((min(a * prime, b), max(a * prime, b)))
                s.add((min(a, b * prime), max(a, b * prime)))
            return s

@functools.lru_cache(maxsize=None)
def factorize_limit(n, lower, upper):
    return [
        (a, b)
        for (a, b) in factorize(n)
        if lower <= a and b <= upper
    ]

@functools.lru_cache(maxsize=None)
def p1(perimeter, lower, upper):
    for width in range(
        max(perimeter - upper, lower),
        min(perimeter - lower, upper, perimeter // 2) + 1,
    ):
        height = perimeter - width
        if len(factorize_limit(width * height, lower, upper)) == 1:
            return False
    return True

@functools.lru_cache(maxsize=None)
def p2(area, lower, upper):
    candidate = None
    for (width, height) in factorize_limit(area, lower, upper):
        if p1(width + height, lower, upper):
            if candidate is not None:
                return None
            candidate = (width, height)
    return candidate

@functools.lru_cache(maxsize=None)
def p3(perimeter, lower, upper):
    candidate = None
    for width in range(
        max(perimeter - upper, lower),
        min(perimeter - lower, upper, perimeter // 2) + 1,
    ):
        height = perimeter - width
        if (width, height) == p2(width * height, lower, upper):
            if candidate is not None:
                return None
            candidate = (width, height)
    return candidate

def solve(lower, upper):
    for perimeter in range(lower*2, upper*2 + 1):
        c = p3(perimeter, lower, upper)
        if c:
            yield c

print(list(solve(1, 15)))
