from tabulate import tabulate

def check(n):
    if all(x == 0 for x in n):
        return 'P1'

    m = [i for i in n if i > 1]
    o = [i for i in n if i == 1]

    if len(m) == 0:
        return 'P1' if len(o) % 2 == 0 else 'P2'

    if len(m) == 1:
        return 'P1'

    return 'P2' if nimsum(n) == 0 else 'P1'


def nimsum(n):
    if not n or all(a == 0 for a in n):
        return 0

    binary = [bin(a)[2:] for a in n if a > 0]
    fakesum = []

    while len(binary) > 0:
        a = sum(int(i[-1]) for i in binary)
        fakesum = [str(a % 2)] + fakesum
        binary = [i[:-1] for i in binary if len(i) > 1]

    if not fakesum:
        return 0
    return int(''.join(fakesum), 2)


def states(h, n):
    """All canonical states: h heaps, total n sticks, sorted ascending."""
    def partitions_at_most(total, max_part):
        if total == 0:
            yield []
            return
        for k in range(min(total, max_part), 0, -1):
            for rest in partitions_at_most(total - k, k):
                yield [k] + rest

    for p in partitions_at_most(n, n):
        if len(p) <= h:
            yield tuple(sorted(p + [0] * (h - len(p))))


def checkall(n, s):
    P1 = 0
    P2 = 0
    for p in states(n, s):
        if check(list(p)) == 'P1':
            P1 += 1
        else:
            P2 += 1

    if P1 + P2 == 0:
        return -1
    return P1 / (P1 + P2)


n = 10
s = 15

mat = [[0 for _ in range(n)] for _ in range(s)]

for i in range(1, n + 1):
    for j in range(1, s + 1):
        mat[j - 1][i - 1] = checkall(i, j)

print(tabulate(
    mat,
    showindex=[f"s={i}" for i in range(1, s + 1)],
    headers=[f"n={i}" for i in range(1, n + 1)],
    tablefmt="grid",
    floatfmt=".6f"
))
