import numpy as np

import itertools


def kernel(i):
    return itertools.islice(
        itertools.cycle(
            itertools.chain(
                itertools.repeat(0, i),
                itertools.repeat(1, i),
                itertools.repeat(0, i),
                itertools.repeat(-1, i),
            )
        ),
        1,
        None,
    )


def convolution(l, i):
    return abs(sum(l_i * k_i for (l_i, k_i) in zip(l, kernel(i)))) % 10


def fft(l):
    return [convolution(l, i + 1) for i in range(len(l))]


def fft_iter(l, times=100):
    for _ in range(times):
        l = fft(l)
    return l


def solve_part1(l):
    solution = fft_iter(l)
    return "".join(str(i) for i in solution[:8])


def fft_iter_2(l, offset, times=100):
    # Key assumption for part 2
    assert offset > 10_000 * len(l) // 2
    # l = np.array([l[i % len(l)] for i in range(offset, 10_000 * len(l))])
    l = np.array(
        list(
            itertools.islice(
                itertools.chain(l[offset % len(l) :], itertools.cycle(l)),
                0,
                10_000 * len(l) - offset,
            )
        )
    )
    l = np.flip(l)
    for i in range(times):
        # simplified ftt computation using linear cumulative sum algorithm, because we
        # have:
        #   fft[i] = sum(l[i] for i in range(i, len(l)))
        np.cumsum(l, out=l)
        np.mod(l, 10, out=l)
    l = np.flip(l)
    return l


def solve_part2(l):
    offset = int("".join(str(i) for i in l[:7]))
    return "".join(str(i) for i in fft_iter_2(l, offset)[:8])


if __name__ == "__main__":
    with open("input") as f:
        content = f.read()

    l = [int(s) for s in content.strip()]

    print(f"Part 1: {solve_part1(l)}")
    print(f"Part 2: {solve_part2(l)}")
