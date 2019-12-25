from copy import deepcopy
from collections import defaultdict, deque
from itertools import combinations


class IntCodeVM:
    VAL, PTR = 0, 1  # arg modes: value / pointer

    INSTRS = {
        1: ("plus", (VAL, VAL, PTR)),
        2: ("mul", (VAL, VAL, PTR)),
        3: ("input", (PTR,)),
        4: ("output", (VAL,)),
        5: ("jump_if_true", (VAL, VAL)),
        6: ("jump_if_false", (VAL, VAL)),
        7: ("less_than", (VAL, VAL, PTR)),
        8: ("equals", (VAL, VAL, PTR)),
        9: ("relative_base_incr", (VAL,)),
        99: ("halt", tuple()),
    }

    def __init__(self, program):
        self.memory = defaultdict(int, {i: elem for i, elem in enumerate(program)})
        self.instr_ptr = 0
        self.relative_base = 0
        self.stdin = deque()
        self.stdout = deque()

    def copy(self):
        return deepcopy(self)

    @property
    def stopped(self):
        return self.memory[self.instr_ptr] == 99

    def arg(self, n, arg_type, arg_mode):
        assert arg_type in [self.VAL, self.PTR]
        assert arg_mode in [0, 1, 2] if arg_type == self.VAL else [0, 2]

        if arg_mode == 0:
            ptr = self.memory[self.instr_ptr + 1 + n]
        elif arg_mode == 1:
            ptr = self.instr_ptr + 1 + n
        elif arg_mode == 2:
            ptr = self.memory[self.instr_ptr + 1 + n] + self.relative_base
        else:
            raise Exception(f"Unknown arg mode: {mode}")

        return ptr if arg_type == self.PTR else self.memory[ptr]

    @classmethod
    def parse_instr(cls, instr):
        opcode = instr % 100
        instr //= 100
        args_types = cls.INSTRS[opcode][1]
        modes = []

        for _ in range(len(args_types)):
            modes.append(instr % 10)
            instr //= 10

        return opcode, modes

    def run(self):
        while not self.stopped:
            opcode, arg_modes = self.parse_instr(self.memory[self.instr_ptr])
            instr_name, arg_types = self.INSTRS[opcode]

            args = [
                self.arg(n, arg_type, arg_mode)
                for n, (arg_type, arg_mode) in enumerate(zip(arg_types, arg_modes))
            ]

            next_instr_ptr = getattr(self, f"op_{instr_name}")(args)
            if next_instr_ptr is None:
                return

            self.instr_ptr = next_instr_ptr

    def op_plus(self, args):
        self.memory[args[2]] = args[0] + args[1]
        return self.instr_ptr + len(args) + 1

    def op_mul(self, args):
        self.memory[args[2]] = args[0] * args[1]
        return self.instr_ptr + len(args) + 1

    def op_input(self, args):
        if not self.stdin:
            return
        self.memory[args[0]] = self.stdin.popleft()
        return self.instr_ptr + len(args) + 1

    def op_output(self, args):
        self.stdout.append(args[0])
        return self.instr_ptr + len(args) + 1

    def op_jump_if_true(self, args):
        return args[1] if args[0] != 0 else self.instr_ptr + len(args) + 1

    def op_jump_if_false(self, args):
        return args[1] if args[0] == 0 else self.instr_ptr + len(args) + 1

    def op_less_than(self, args):
        self.memory[args[2]] = 1 if args[0] < args[1] else 0
        return self.instr_ptr + len(args) + 1

    def op_equals(self, args):
        self.memory[args[2]] = 1 if args[0] == args[1] else 0
        return self.instr_ptr + len(args) + 1

    def op_relative_base_incr(self, args):
        self.relative_base += args[0]
        return self.instr_ptr + len(args) + 1

    def op_halt(self, args):
        return


def solve_part1(program):
    vm = IntCodeVM(program)

    # uncomment the following lines to play the game manually
    # you need to find the 8 items and the room with the weight sensor
    # commands = []
    # while True:
    #     vm.run()
    #     output = "".join(chr(s) for s in vm.stdout)
    #     print(output, end="")
    #     command = input()
    #     if command == "show":
    #         print(commands)
    #     else:
    #         vm.stdin.extend(ord(s) for s in command + "\n")

    setup_commands = [
        "north",
        "south",
        "east",
        "east",
        "take semiconductor",
        "north",
        "take planetoid",
        "north",
        "take antenna",
        "west",
        "east",
        "south",
        "west",
        "take food ration",
        "west",
        "west",
        "take monolith",
        "east",
        "east",
        "east",
        "west",
        "north",
        "take space law space brochure",
        "north",
        "north",
        "take weather machine",
        "south",
        "south",
        "south",
        "north",
        "east",
        "take jam",
        "west",
        "south",
        "east",
        "inv",
        "south",
        "west",
        "east",
        "east",
        "south",
        "south",
        "east",
        "inv",
    ]
    vm.stdin.extend(ord(s) for s in "\n".join(setup_commands) + "\n")

    items = [
        "food ration",
        "weather machine",
        "antenna",
        "space law space brochure",
        "jam",
        "semiconductor",
        "planetoid",
        "monolith",
    ]
    picked_items = tuple(items)
    tries = (
        combination
        for i in range(1, len(items) + 1)
        for combination in combinations(items, i)
    )
    for combination in tries:
        commands = []
        for item in combination:
            if item not in picked_items:
                commands.append(f"take {item}")
        for item in picked_items:
            if item not in combination:
                commands.append(f"drop {item}")
        picked_items = combination
        commands.append("inv")
        commands.append("east")
        vm.stdin.extend(ord(s) for s in "\n".join(commands) + "\n")
        vm.run()
        output = "".join(chr(s) for s in vm.stdout)
        print(output, end="")
        vm.stdout = deque()
        if "lighter" not in output and "heavier" not in output:
            return


if __name__ == "__main__":
    with open("input") as f:
        content = f.read()

    program = list(map(int, content.split(",")))
    solve_part1(program)

