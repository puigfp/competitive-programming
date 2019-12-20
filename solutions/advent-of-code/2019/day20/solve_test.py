from solve import solve_part1, solve_part2


mazes = dict()

for name in ["small", "medium", "large"]:
    with open(f"input_{name}") as f:
        mazes[name] = f.read().rstrip().splitlines()


def test_solve_part1():
    mazes_ = [mazes["small"], mazes["medium"]]
    expected = [23, 58]
    for maze, expected in zip(mazes_, expected):
        assert solve_part1(maze) == expected


def test_solve_part2():
    mazes_ = [mazes["small"], mazes["large"]]
    expected = [26, 396]
    for maze, expected in zip(mazes_, expected):
        assert solve_part2(maze) == expected
