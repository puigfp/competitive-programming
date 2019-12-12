from functools import reduce
from math import gcd


def parse_input(s):
    positions = []
    for line in s.splitlines():
        numbers = line.strip()[1:-1].split(",")
        positions.append(tuple(int(n.split("=")[1]) for n in numbers))
    return positions


def new_velocities(positions, velocities):
    for i in range(len(positions)):
        for j in range(len(positions)):
            velocities[i] = tuple(
                velocities[i][k]
                + (
                    1
                    if positions[i][k] < positions[j][k]
                    else -1
                    if positions[i][k] > positions[j][k]
                    else 0
                )
                for k in range(3)
            )
    return velocities


def new_positions(positions, velocities):
    return [
        (p[0] + v[0], p[1] + v[1], p[2] + v[2]) for p, v in zip(positions, velocities)
    ]


def energy(positions, velocities):
    return sum(
        sum(map(abs, p)) * sum(map(abs, v)) for p, v in zip(positions, velocities)
    )


def solve_part1(positions, steps=1000):
    velocities = [(0, 0, 0) for _ in range(len(positions))]
    for _ in range(steps):
        velocities = new_velocities(positions, velocities)
        positions = new_positions(positions, velocities)
    return energy(positions, velocities)


def find_repeat(positions):
    states = set()
    velocities = [0 for _ in range(len(positions))]
    while True:
        # store current state in state history
        save = (tuple(positions), tuple(velocities))
        if save in states:
            return len(states)
        states.add(save)

        # update velocities
        for i in range(len(positions)):
            for j in range(len(positions)):
                velocities[i] += (
                    1
                    if positions[i] < positions[j]
                    else -1
                    if positions[i] > positions[j]
                    else 0
                )

        # update positions
        for i in range(len(positions)):
            positions[i] += velocities[i]


def solve_part2(positions):
    repeats = [find_repeat([e[i] for e in positions]) for i in range(3)]
    # lowest common multiple
    return reduce(lambda x, y: x * y // gcd(x, y), repeats)


if __name__ == "__main__":
    with open("input") as f:
        content = f.read()

    positions = parse_input(content)
    print(f"Part 1: {solve_part1(positions)}")
    print(f"Part 2: {solve_part2(positions)}")
