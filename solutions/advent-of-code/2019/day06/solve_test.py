from solve import solve_part1, lines_to_graph_part1, lines_to_graph_part2, solve_part2


def test_solve_part1():
    lines = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
    assert solve_part1(lines_to_graph_part1(lines.splitlines())) == 42


def test_solve_part2():
    lines = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
    assert solve_part2(lines_to_graph_part2(lines.splitlines())) == 4
