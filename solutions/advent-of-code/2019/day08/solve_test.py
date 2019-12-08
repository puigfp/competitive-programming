from solve import parse_image, solve_part1


def test_parse_image():
    assert parse_image("123456789012", 2, 3) == [
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [0, 1, 2]],
    ]


def test_solve_part1():
    assert solve_part1(parse_image("123456789012", 2, 3)) == 1
