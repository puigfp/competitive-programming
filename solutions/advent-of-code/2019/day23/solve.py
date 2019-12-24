from copy import deepcopy
from collections import defaultdict, deque


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
    n = 50
    vms = [IntCodeVM(program) for _ in range(50)]

    for i, vm in enumerate(vms):
        vm.stdin.append(i)

    while True:
        for i, vm in enumerate(vms):
            assert vm.stopped == False

            if not vm.stopped and not vm.stdin:
                vm.stdin.append(-1)

            vm.run()
            assert len(vm.stdout) % 3 == 0

            while vm.stdout:
                dest, X, Y = (vm.stdout.popleft() for _ in range(3))
                if dest == 255:
                    return Y
                vms[dest].stdin.extend([X, Y])


def solve_part2(program):
    n = 50
    vms = [IntCodeVM(program) for _ in range(50)]

    for i, vm in enumerate(vms):
        vm.stdin.append(i)

    X_nat, Y_nat = None, None  # next values to be delivered by the NAT
    Y_delivered = None  # last Y value delivered by the NAT

    while True:
        idle = True

        for i, vm in enumerate(vms):
            assert vm.stopped == False

            if not vm.stopped and not vm.stdin:
                vm.stdin.append(-1)
            else:
                idle = False

            vm.run()
            assert len(vm.stdout) % 3 == 0

            if vm.stdout:
                idle = False

            while vm.stdout:
                dest, X, Y = (vm.stdout.popleft() for _ in range(3))
                if dest == 255:
                    X_nat, Y_nat = X, Y
                else:
                    vms[dest].stdin.extend([X, Y])

        if idle:
            if Y_delivered is not None and Y_delivered == Y_nat:
                return Y_delivered
            Y_delivered = Y_nat
            vms[0].stdin.extend([X_nat, Y_nat])


if __name__ == "__main__":
    with open("input") as f:
        content = f.read()

    program = list(map(int, content.split(",")))

    print(f"Part 1: {solve_part1(program)}")
    print(f"Part 2: {solve_part2(program)}")

