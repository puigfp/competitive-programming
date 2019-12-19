from random import randint, choice
from string import ascii_lowercase

N = 100_000
M = 100_000

lines = []

lines.append(str(N))
for i in range(1, N):
    lines.append(f"{i} {i+1}")

lines.append("".join(choice(ascii_lowercase) for _ in range(N)))

lines.append(str(M))
for i in range(M):
    if i % 2 == 0:
        lines.append(f"0 {randint(1, N)} {choice(ascii_lowercase)}")
    else:
        lines.append(f"1 {randint(1, N)}")


with open("input_random.txt", "w") as f:
    f.write("\n".join(lines))
