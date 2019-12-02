import copy


def execute(program):
    program = copy.copy(program)
    i = 0
    while program[i] != 99:
        assert program[i] in [1, 2]
        if program[i] == 1:
            program[program[i + 3]] = program[program[i + 1]] + program[program[i + 2]]
        elif program[i] == 2:
            program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
        i += 4
    return program


def find_inputs(desired_output, program):
    for noun in range(100):
        for verb in range(100):
            program[1] = noun
            program[2] = verb
            final_state = execute(program)
            if final_state[0] == desired_output:
                return noun, verb
    return None


if __name__ == "__main__":
    with open("input") as f:
        content = f.readlines()
    assert len(content) == 1
    program = [int(n) for n in content[0].split(",")]

    # Part 1
    program[1] = 12
    program[2] = 2
    final_state = execute(program)
    print(f"Part 1: {final_state[0]}")

    # Part 2
    (noun, verb) = find_inputs(1969_07_20, program)
    print(f"Part 2: {100 * noun + verb}")
