from solve import ok, ok_2


def test_ok():
    tests = [(111111, True), (223450, False), (123789, False)]
    for (a, b) in tests:
        assert ok(a) == b


def test_ok_2():
    tests = [
        (111111, False),
        (223450, False),
        (123789, False),
        (112233, True),
        (123444, False),
        (111122, True),
    ]
    for (a, b) in tests:
        assert ok_2(a) == b
