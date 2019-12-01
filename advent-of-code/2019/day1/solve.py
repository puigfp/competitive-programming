def required_fuel(mass):
    return mass // 3 - 2


def required_fuel_2(mass):
    requirement = required_fuel(mass)
    if requirement < 0:
        return 0
    return requirement + required_fuel_2(requirement)


def solve_part1(masses):
    return sum(required_fuel(mass) for mass in masses)


def solve_part2(masses):
    return sum(required_fuel_2(mass) for mass in masses)


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()
    masses = [int(line) for line in lines]
    print(f"Part 1: {solve_part1(masses)}")
    print(f"Part 2: {solve_part2(masses)}")
