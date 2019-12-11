from collections import defaultdict


def execute(state, input_):
    program, i, j, relative_base = state
    output = []
    while program[i] != 99:
        opcode = program[i] % 100

        modes = {
            1: (program[i] // 100) % 10,
            2: (program[i] // 1000) % 10,
            3: (program[i] // 10000) % 10,
        }

        def param(n):
            if modes[n] == 0:
                return program[program[i + n]]
            elif modes[n] == 1:
                return program[i + n]
            elif modes[n] == 2:
                return program[program[i + n] + relative_base]
            else:
                raise f"Invalid param mode: {modes[n]}"

        def param_addr(n):
            if modes[n] == 0:
                return program[i + n]
            elif modes[n] == 2:
                return program[i + n] + relative_base
            else:
                raise f"Invalid param mode: {modes[n]}"

        if opcode == 1:  # plus
            program[param_addr(3)] = param(1) + param(2)
            i += 4
        elif opcode == 2:  # mul
            program[param_addr(3)] = param(1) * param(2)
            i += 4
        elif opcode == 3:  # input
            # no more inputs: exit at current state
            if j >= len(input_):
                return (program, i, 0, relative_base), output
            program[param_addr(1)] = input_[j]
            j += 1
            i += 2
        elif opcode == 4:  # output
            output.append(param(1))
            i += 2
        elif opcode == 5:  # jump if true
            if param(1) != 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 6:  #  jump if false
            if param(1) == 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 7:  # less than
            program[param_addr(3)] = 1 if param(1) < param(2) else 0
            i += 4
        elif opcode == 8:  # equals
            program[param_addr(3)] = 1 if param(1) == param(2) else 0
            i += 4
        elif opcode == 9:  # relative base update
            relative_base += param(1)
            i += 2
        else:
            raise f"Invalid opcode: {opcode}"

    return (program, i, 0, relative_base), output


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up  # right  # down  # left


def run(program, color):
    universe = defaultdict(lambda: 0)
    position = (0, 0)
    direction = 0

    universe[position] = color

    state = defaultdict(lambda: 0, {i: e for i, e in enumerate(program)}), 0, 0, 0

    while True:
        state, output = execute(state, [universe[position]])

        if len(output) == 0:
            break

        assert len(output) == 2

        color, turn = output

        # paint
        universe[position] = color

        # turn
        assert turn in [0, 1]
        direction += -1 if turn == 0 else 1
        direction %= 4

        # move
        position = (
            position[0] + directions[direction][0],
            position[1] + directions[direction][1],
        )

    return universe


def solve_part1(program):
    return len(run(program, 0))


def solve_part2(program):
    universe = run(program, 1)
    min_x, max_x = min(pos[0] for pos in universe), max(pos[0] for pos in universe)
    min_y, max_y = min(pos[1] for pos in universe), max(pos[1] for pos in universe)
    return "\n".join(
        "".join(" " if universe[(x, y)] == 0 else "#" for y in range(min_y, max_y + 1))
        for x in range(min_x, max_x + 1)
    )


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()

    assert len(lines) == 1
    program = list(map(int, lines[0].split(",")))

    print(f"Part 1: {solve_part1(program)}")
    print(f"Part 2:\n{solve_part2(program)}")
