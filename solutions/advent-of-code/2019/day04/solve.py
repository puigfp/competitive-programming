from functools import reduce


def ok(password):
    password_str = str(password)

    # no need to check the range conditions

    if not any(
        password_str[i - 1] == password_str[i] for i in range(1, len(password_str))
    ):
        return False

    if not all(
        password_str[i - 1] <= password_str[i] for i in range(1, len(password_str))
    ):
        return False

    return True


def ok_2(password):
    password_str = str(password)

    # no need to check the range conditions

    if not all(
        password_str[i - 1] <= password_str[i] for i in range(1, len(password_str))
    ):
        return False

    count = 1
    counts = []
    last = password_str[0]

    for i in range(1, len(password_str)):
        if password_str[i] == last:
            count += 1
        else:
            counts.append(count)
            count = 1
            last = password_str[i]

    counts.append(count)  # password = 111122 => counts = [4, 2]

    if 2 not in counts:
        return False

    return True


def solve_part1(min_, max_):
    # len(filter)
    return reduce(lambda sum_, _: sum_ + 1, filter(ok, range(min_, max_ + 1)), 0)


def solve_part2(min_, max_):
    # len(filter)
    return reduce(lambda sum_, _: sum_ + 1, filter(ok_2, range(min_, max_ + 1)), 0)


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()

    min_, max_ = map(int, lines[0].split("-"))
    assert 100000 <= min_ <= 999999
    assert 100000 <= max_ <= 999999

    print(f"Part 1: {solve_part1(min_, max_)}")
    print(f"Part 2: {solve_part2(min_, max_)}")
