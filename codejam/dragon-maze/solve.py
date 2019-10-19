from collections import defaultdict

def solve(maze, start, finish):
    """
    Solve is a BFS.

    At the beginning of iteration i:
        - current_step keys are all the cells whose whose shortest path from the
            entrance is i cells long.
        - current_step[cell] contains the maximum amount of power we can gather on our
            way to a given cell
        - seen contains all the cells whose shortest path from the entrance is j cells
            long with j <= i
    """
    current_step = {
        start: maze[start[0]][start[1]]
    }
    next_step = dict()
    seen = { start }

    ok = lambda cell: \
        0 <= cell[0] < len(maze) and \
        0 <= cell[1] < len(maze[0]) and \
        maze[cell[0]][cell[1]] >= 0 and \
        cell not in seen

    def next_cells(cell):
        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        plus = lambda cell, delta: tuple(e1 + e2 for (e1, e2) in zip (cell, delta))

        for delta in deltas:
            next_cell = plus(cell, delta)
            if ok(next_cell):
                yield next_cell

    while current_step:
        if finish in current_step:
            return current_step[finish]

        for cell, power in current_step.items():
            for next_cell in next_cells(cell):
                next_step[next_cell] = max(
                    next_step.get(next_cell, float('-inf')),
                    power + maze[next_cell[0]][next_cell[1]],
                )

        current_step, next_step = next_step, dict()
        seen = seen.union(set(current_step))

    return None

T = int(input())
for i in range(T):
    N, M = map(int, input().split())
    Xs, Ys, Xf, Yf = map(int, input().split())
    start = (Xs, Ys)
    finish = (Xf, Yf)
    maze = [
        list(map(int, input().split()))
        for _ in range(N)
    ]
    solution = solve(maze, start, finish)
    print(f"Case #{i+1}: {solution if solution is not None else 'Mission Impossible.'}")
