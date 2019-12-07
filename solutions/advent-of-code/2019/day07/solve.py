import copy
import itertools


def execute(state, input_):
    program, i, j = state
    output = []
    while program[i] != 99:
        opcode = program[i] % 100
        assert 1 <= opcode <= 8

        param_mode_1 = (program[i] // 100) % 10
        param_mode_2 = (program[i] // 1000) % 10
        param_mode_3 = (program[i] // 10000) % 10

        param_1 = program[program[i + 1]] if param_mode_1 == 0 else program[i + 1]
        if opcode in [1, 2, 5, 6, 7, 8]:
            param_2 = program[program[i + 2]] if param_mode_2 == 0 else program[i + 2]

        if opcode == 1:  # plus
            assert param_mode_3 == 0
            program[program[i + 3]] = param_1 + param_2
            i += 4
        elif opcode == 2:  # mul
            assert param_mode_3 == 0
            program[program[i + 3]] = param_1 * param_2
            i += 4
        elif opcode == 3:  # input
            assert param_mode_1 == 0

            # no more inputs available
            if j >= len(input_):
                return (program, i, j), output

            program[program[i + 1]] = input_[j]
            j += 1
            i += 2
        elif opcode == 4:  # output
            output.append(param_1)
            i += 2
        elif opcode == 5:  # jump if true
            if param_1 != 0:
                i = param_2
            else:
                i += 3
        elif opcode == 6:  #  ump if false
            if param_1 == 0:
                i = param_2
            else:
                i += 3
        elif opcode == 7:  # less than
            assert param_mode_3 == 0
            program[program[i + 3]] = 1 if param_1 < param_2 else 0
            i += 4
        elif opcode == 8:  # equals
            assert param_mode_3 == 0
            program[program[i + 3]] = 1 if param_1 == param_2 else 0
            i += 4

    return (program, i, j), output


def signal_part1(program, phases):
    input_ = 0
    for phase in phases:
        _, output = execute([copy.copy(program), 0, 0], [phase, input_])
        assert len(output) == 1
        input_ = output[0]
    return input_


def solve_part1(program):
    return max(
        (signal_part1(program, phases) for phases in itertools.permutations(range(5)))
    )


def signal_part2(program, phases):
    inputs = [[phase] for phase in phases]
    inputs[0].append(0)
    states = [(copy.copy(program), 0, 0) for phase in phases]

    while True:
        for i in range(5):
            states[i], output = execute(states[i], inputs[i])
            inputs[(i + 1) % len(inputs)] += output

            if len(output) == 0:
                # the last output of the last amplifier is the last input of the first one
                return inputs[0][-1]


def solve_part2(program):
    return max(
        (
            signal_part2(program, phases)
            for phases in itertools.permutations(range(5, 10))
        )
    )


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()
    assert len(lines) == 1

    program = list(map(int, lines[0].split(",")))

    print(f"Part 1: {solve_part1(program)}")
    print(f"Part 2: {solve_part2(program)}")
