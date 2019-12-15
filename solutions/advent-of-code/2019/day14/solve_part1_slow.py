from collections import deque
import heapq
import re


ORE = "ORE"
FUEL = "FUEL"

line_regexp = re.compile(r"(\d+) (\w+)")


def parse_line(line):
    left_right = line.strip().split("=>")
    left_right_matches = [line_regexp.findall(part) for part in left_right]
    return tuple(
        {name: int(number) for number, name in matches}
        for matches in left_right_matches
    )


def parse_file(s):
    return [parse_line(line) for line in s.splitlines()]


def hash_dict(d):
    return hash(frozenset(d.items()))


def is_transformation_doable(resources, transformation):
    input_, output = transformation
    return all(
        chemical == ORE or quantity <= resources.get(chemical, 0)
        for chemical, quantity in input_.items()
    )


def do_transformation(state, transformation):
    used_ore, _, resources = state
    input_, output = transformation
    resources = resources.copy()

    for chemical, quantity in input_.items():
        if chemical == ORE:
            used_ore += quantity
        else:
            resources[chemical] -= quantity
            assert resources[chemical] >= 0

    for chemical, quantity in output.items():
        resources[chemical] = resources.get(chemical, 0) + quantity

    return used_ore, hash_dict(resources), resources


def solve_part1(transformations):
    q = [(0, hash_dict({}), {})]

    seen = set()

    transformations_ore = [
        (input_, output) for (input_, output) in transformations if ORE in input_
    ]
    transformations = [
        (input_, output) for (input_, output) in transformations if ORE not in input_
    ]

    while q:
        state = heapq.heappop(q)
        used_ore, _, resources = state
        if resources.get(FUEL, 0) >= 1:
            return used_ore

        doable_transformations = [
            t for t in transformations if is_transformation_doable(resources, t)
        ]
        next_transformations = (
            doable_transformations
            if len(doable_transformations) > 0
            else transformations_ore
        )
        for transformation in next_transformations:
            next_state = do_transformation(state, transformation)
            if next_state[1] not in seen:
                heapq.heappush(q, next_state)
                seen.add(next_state[1])
