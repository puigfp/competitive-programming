from collections import deque

def solve(maze, start, finish):
    """
    Solve is a BFS.

    We use the state variable to keep track of the shortest paths.

    state[i][j][0] =
        length of shortest path from start to (i, j), None if (i, j) hasn't been seen yet

    state[i][j][1] =
        maximum power we can gather by going from start to (i, j) following one of the
        shortest paths, None if (i, j) hasn't been seen yet
    """
    state = [
        [
            (None, None)
            for _ in range(len(maze[0]))
        ]
        for _ in range(len(maze))
    ]

    q = deque([ start ])
    state[start[0]][start[1]] = (0, maze[start[0]][start[1]])

    ok = lambda cell, k: \
        0 <= cell[0] < len(maze) and \
        0 <= cell[1] < len(maze[0]) and \
        maze[cell[0]][cell[1]] >= 0 and \
        (state[cell[0]][cell[1]][0] is None or state[cell[0]][cell[1]][0] == k)

    def next_cells(cell, k):
        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        plus = lambda cell, delta: tuple(e1 + e2 for (e1, e2) in zip (cell, delta))

        for delta in deltas:
            next_cell = plus(cell, delta)
            if ok(next_cell, k):
                yield next_cell

    while q:
        cell = q.popleft()
        k, power = state[cell[0]][cell[1]]
        for next_cell in next_cells(cell, k + 1):
            if state[next_cell[0]][next_cell[1]][0] is None:
                q.append(next_cell)
            state[next_cell[0]][next_cell[1]] = (
                k + 1,
                max(
                    state[next_cell[0]][next_cell[1]][1] or float('-inf'),
                    power + maze[next_cell[0]][next_cell[1]]
                )
            )

    return state[finish[0]][finish[1]][1]

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
