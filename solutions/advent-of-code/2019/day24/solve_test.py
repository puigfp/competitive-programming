import numpy as np

from solve import solve_part1, solve_part2, biodiversity_rating, parse_input


def test_biodiversity_rating():
    state = """
    .....
    .....
    .....
    #....
    .#...
    """
    assert biodiversity_rating(parse_input(state)) == 2129920


def test_solve_part1():
    state = """
    ....#
    #..#.
    #..##
    ..#..
    #....
    """
    assert solve_part1(parse_input(state)) == 2129920


def test_solve_part2():
    state = """
    ....#
    #..#.
    #..##
    ..#..
    #....
    """
    assert solve_part2(parse_input(state), minutes=10) == 99

