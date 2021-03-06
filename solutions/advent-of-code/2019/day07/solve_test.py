import copy

from solve import execute, solve_part1, solve_part2


def test_execute():
    tests = [
        ([3, 0, 4, 0, 99], [11], [11]),
        ([3, 0, 4, 0, 99], [12], [12]),
        ([1101, 100, -1, 0, 4, 0, 99], [], [99]),
        # == 8
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8], [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [9], [0]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7], [0]),
        # < 8
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7], [1]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8], [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [9], [0]),
        # == 8
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8], [1]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [9], [0]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [7], [0]),
        # < 8
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7], [1]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8], [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [9], [0]),
        # != 0
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [11], [1]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0], [0]),
        # != 0
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [11], [1]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0], [0]),
        # larger example
        # fmt: off
        ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [5], [999]),
        ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [8], [1000]),
        ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [11], [1001]),
        # fmt: on
    ]

    for program, input_, output in tests:
        assert execute([copy.copy(program), 0, 0], input_)[1] == output


def test_solve_part1():
    tests = [
        # fmt: off
        ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], 43210),
        ([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], 54321),
        ([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], 65210),
        # fmt: on
    ]
    for program, highest_signal in tests:
        assert solve_part1(program) == highest_signal


def test_solve_part2():
    tests = [
        # fmt: off
        ([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 139629729),
        ([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 18216),
        # fmt: on
    ]
    for program, highest_signal in tests:
        assert solve_part2(program) == highest_signal
