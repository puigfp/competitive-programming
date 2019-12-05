import copy


def execute(program, input_):
    program = copy.copy(program)
    output = []
    i = 0
    j = 0
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

    return output


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()

    program = list(map(int, lines[0].split(",")))

    output_1 = execute(program, [1])
    # all elements but the last should be null
    assert all(map(lambda i: i == 0, output_1[:-1]))
    print(f"Part 1: {output_1[-1]}")

    output_2 = execute(program, [5])
    assert len(output_2) == 1
    print(f"Part 1: {output_2[0]}")
