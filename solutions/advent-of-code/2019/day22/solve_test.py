import math

from solve import parse_input, apply_operations, euclid, apply_operations_alt


def test_apply_operations():
    tests = [
        ("deal into new stack", "9 8 7 6 5 4 3 2 1 0"),
        ("cut 3", "3 4 5 6 7 8 9 0 1 2"),
        ("cut -4", "6 7 8 9 0 1 2 3 4 5"),
        ("deal with increment 3", "0 7 4 1 8 5 2 9 6 3"),
        (
            """
deal with increment 7
deal into new stack
deal into new stack
            """,
            "0 3 6 9 2 5 8 1 4 7",
        ),
        (
            """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
            """,
            "9 2 5 8 1 4 7 0 3 6",
        ),
    ]

    for s, result in tests:
        operations = parse_input(s)
        result = [int(s) for s in result.split()]
        deck = list(range(len(result)))
        assert apply_operations(deck, operations) == result
        assert [
            apply_operations_alt(position, len(deck), operations) for position in deck
        ] == result


def test_euclid():
    tests = [(5, 0), (0, 5), (10, 11), (417829, 4128974)]

    for a, b in tests:
        x, y, gcd = euclid(a, b)
        assert gcd == math.gcd(a, b)
        assert a * x + b * y == gcd
