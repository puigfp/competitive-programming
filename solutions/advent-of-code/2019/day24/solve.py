import numpy as np


def parse_input(s):
    return np.array(
        [[0 if s == "." else 1 for s in line.strip()] for line in s.strip().split("\n")]
    )


def adjacent_bugs(state):
    bugs = np.zeros_like(state)
    bugs[1:, :] += state[:-1, :]
    bugs[:-1, :] += state[1:, :]
    bugs[:, 1:] += state[:, :-1]
    bugs[:, :-1] += state[:, 1:]
    return bugs


def biodiversity_rating(state):
    rating = 0
    incr = 1
    for i in state.flat:
        rating += i * incr
        incr <<= 1
    return rating


def solve_part1(state):
    history = set([biodiversity_rating(state)])
    while True:
        bugs = adjacent_bugs(state)
        to_zero = (state == 1) * (bugs != 1)
        to_one = (state == 0) * ((bugs == 1) + (bugs == 2))
        state[to_zero] = 0
        state[to_one] = 1
        rating = biodiversity_rating(state)
        if rating in history:
            return rating
        history.add(rating)


def adjacent_bugs_2(state):
    bugs = np.zeros_like(state)
    # almost a copy-paste from adjacent_bugs
    bugs[:, 1:, :] += state[:, :-1, :]
    bugs[:, :-1, :] += state[:, 1:, :]
    bugs[:, :, 1:] += state[:, :, :-1]
    bugs[:, :, :-1] += state[:, :, 1:]
    bugs[:, 2, 2] = 0  # center cannot become a bug

    # level recursion
    bugs[1:, :, 0] += state[:-1, 2, 1].reshape(-1, 1)
    bugs[1:, :, 4] += state[:-1, 2, 3].reshape(-1, 1)
    bugs[1:, 0, :] += state[:-1, 1, 2].reshape(-1, 1)
    bugs[1:, 4, :] += state[:-1, 3, 2].reshape(-1, 1)
    bugs[:-1, 2, 1] += state[1:, :, 0].sum(axis=1)
    bugs[:-1, 2, 3] += state[1:, :, 4].sum(axis=1)
    bugs[:-1, 1, 2] += state[1:, 0, :].sum(axis=1)
    bugs[:-1, 3, 2] += state[1:, 4, :].sum(axis=1)

    return bugs


def print_state(state):
    delta = (state.shape[0] - 1) // 2
    for i, level in enumerate(state):
        print(f"Level {i-delta}")
        print(
            "\n".join("".join("#" if c == 1 else "." for c in line) for line in level)
        )


def solve_part2(state, minutes=200):
    state = state.reshape(-1, 5, 5)
    state = np.vstack(
        [np.zeros_like(state) for _ in range(minutes // 2)]
        + [state]
        + [np.zeros_like(state) for _ in range(minutes // 2)]
    )

    for _ in range(minutes):
        bugs = adjacent_bugs_2(state)
        to_zero = (state == 1) * (bugs != 1)
        to_one = (state == 0) * ((bugs == 1) + (bugs == 2))
        state[to_zero] = 0
        state[to_one] = 1

    return state.sum()


if __name__ == "__main__":
    with open("input") as f:
        content = f.read()
    state = parse_input(content)
    print(f"Part 1: {solve_part1(state.copy())}")
    print(f"Part 2: {solve_part2(state.copy())}")
