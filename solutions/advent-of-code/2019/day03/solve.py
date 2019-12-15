directions = {"R": (0, 1), "U": (1, 0), "L": (0, -1), "D": (-1, 0)}


def compute_coords(path):
    current_position = (0, 0)
    total_steps = 0
    cable = dict()  # (x, y) -> steps
    for line in path:
        direction = line[0]
        steps = int(line[1:])
        for step in range(steps):
            current_position = (
                current_position[0] + directions[direction][0],
                current_position[1] + directions[direction][1],
            )
            total_steps += 1
            if current_position not in cable:
                cable[current_position] = total_steps
    return cable


def solve_part1(coords1, coords2):
    intersections = set(coords1).intersection(coords2)
    return min(abs(c[0]) + abs(c[1]) for c in intersections)


def solve_part2(coords1, coords2):
    intersections = set(coords1).intersection(coords2)
    return min(coords1[c] + coords2[c] for c in intersections)


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()
    coords1, coords2 = [compute_coords(line.split(",")) for line in lines]
    print(f"Part 1: {solve_part1(coords1, coords2)}")
    print(f"Part 2: {solve_part2(coords1, coords2)}")
