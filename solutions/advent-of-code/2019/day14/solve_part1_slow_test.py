from solve_part1_slow import (
    parse_line,
    parse_file,
    is_transformation_doable,
    do_transformation,
    solve_part1,
    ORE,
)


def test_parse_line():
    tests = [
        ("4 ZDGD, 1 HTRQV => 3 VRKNQ", ({"ZDGD": 4, "HTRQV": 1}, {"VRKNQ": 3})),
        ("15 XKZQZ, 1 MWZQ => 4 LHWX", ({"XKZQZ": 15, "MWZQ": 1}, {"LHWX": 4})),
    ]

    for line, expected_output in tests:
        assert parse_line(line) == expected_output


def test_is_transformation_doable():
    tests = [
        ({"A": 10, "B": 5}, ({"A": 1, "B": 1, "C": 1}, {"D": 1}), False),
        ({"A": 10, "B": 5}, ({"A": 1, "B": 6}, {"D": 1}), False),
        ({"A": 10, "B": 5}, ({"A": 10, "B": 1}, {"D": 1}), True),
        ({}, ({ORE: 1}, {"D": 1}), True),
    ]
    for resources, transformation, expected_output in tests:
        assert is_transformation_doable(resources, transformation) == expected_output


def test_do_transformation():
    tests = [
        (
            (5, {"A": 10, "B": 5}),
            ({"A": 10, "B": 1}, {"D": 1}),
            (5, {"A": 0, "B": 4, "D": 1}),
        ),
        ((0, {}), ({ORE: 1}, {"D": 1}), (1, {"D": 1})),
    ]
    for state, transformation, expected_output in tests:
        used_ore, _, resources = do_transformation(
            (state[0], 0, state[1]), transformation
        )
        assert (used_ore, resources) == expected_output
        assert resources != expected_output, "Input got mutated"


def test_solve_part1():
    tests = [
        (
            """9 ORE => 2 A
            8 ORE => 3 B
            7 ORE => 5 C
            3 A, 4 B => 1 AB
            5 B, 7 C => 1 BC
            4 C, 1 A => 1 CA
            2 AB, 3 BC, 4 CA => 1 FUEL""",
            165,
        ),
        # (
        #     """157 ORE => 5 NZVS
        #     165 ORE => 6 DCFZ
        #     44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        #     12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        #     179 ORE => 7 PSHF
        #     177 ORE => 5 HKGWZ
        #     7 DCFZ, 7 PSHF => 2 XJWVT
        #     165 ORE => 2 GPVTF
        #     3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""",
        #     13312,
        # ),
        # (
        #     """
        #     2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        #     17 NVRVD, 3 JNWZP => 8 VPVL
        #     53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        #     22 VJHF, 37 MNCFX => 5 FWMGM
        #     139 ORE => 4 NVRVD
        #     144 ORE => 7 JNWZP
        #     5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        #     5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        #     145 ORE => 6 MNCFX
        #     1 NVRVD => 8 CXFTF
        #     1 VJHF, 6 MNCFX => 4 RFSQX
        #     176 ORE => 6 VJHF""",
        #     180697,
        # ),
    ]

    for s, solution in tests:
        assert solve_part1(parse_file(s)) == solution
