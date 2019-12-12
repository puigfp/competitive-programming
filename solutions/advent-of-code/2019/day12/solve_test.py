from solve import solve_part1, solve_part2


def test_solve_part1():
    tests = [
        ([(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)], 10, 179),
        ([(-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)], 100, 1940),
    ]
    for positions, steps, solution in tests:
        assert solve_part1(positions, steps) == solution


def test_solve_part2():
    tests = [
        ([(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)], 2772),
        ([(-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)], 4686774924),
    ]
    for positions, solution in tests:
        assert solve_part2(positions) == solution
