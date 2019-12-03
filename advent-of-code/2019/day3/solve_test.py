from solve import compute_coords, solve_part1, solve_part2

tests = [
    (("R8,U5,L5,D3", "U7,R6,D4,L4"), (6, 30)),
    (
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"),
        (159, 610),
    ),
    (
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ),
        (135, 410),
    ),
]


def test_solve():
    for (cables, (part1, part2)) in tests:
        coords1, coords2 = [compute_coords(line.split(",")) for line in cables]
        assert solve_part1(coords1, coords2) == part1
        assert solve_part2(coords1, coords2) == part2
