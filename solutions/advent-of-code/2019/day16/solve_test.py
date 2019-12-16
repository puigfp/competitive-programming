import itertools

from solve import kernel, fft, solve_part1, solve_part2


def test_kernel():
    tests = [
        (3, [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1])
    ]

    for i, expected_output in tests:
        assert (
            list(itertools.islice(kernel(i), 0, len(expected_output)))
            == expected_output
        )


def test_fft():
    tests = [
        ("12345678", "48226158"),
        ("48226158", "34040438"),
        ("34040438", "03415518"),
        ("03415518", "01029498"),
    ]

    cast = lambda l: list(map(int, l))
    for input_, expected_output in tests:
        assert fft(cast(input_)) == cast(expected_output)


def test_solve_part1():
    tests = [
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ]

    cast = lambda l: list(map(int, l))
    for input_, expected_output in tests:
        assert solve_part1(cast(input_)) == expected_output


def test_solve_part2():
    tests = [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ]

    cast = lambda l: list(map(int, l))
    for input_, expected_output in tests:
        assert solve_part2(cast(input_)) == expected_output
