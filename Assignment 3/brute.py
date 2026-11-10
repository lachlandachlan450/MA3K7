def check(n):
    if n == [0 for i in n]:
        return 'P1'
    m = [i for i in n if i>1]
    o = [i for i in n if i==1]
    if len(m) == 0:
        if len(o) % 2 == 0:
            return 'P1'
        else:
            return 'P2'
    if len(m) == 1:
        return 'P1'
    else:
        if nimsum(n) == 0:
            return 'P2'
        else:
            return 'P1'

def nimsum(n):
    if not n or all(a == 0 for a in n):
        return 0
    binary = [bin(a)[2:] for a in n if a > 0]
    fakesum = []
    while len(binary) > 0:
        a = sum([int(i[-1]) for i in binary])
        if a % 2 == 0:
            fakesum = ['0'] + fakesum
        else:
            fakesum = ['1'] + fakesum
        binary = [i[:-1] for i in binary if len(i) > 1]
    if not fakesum:
        return 0
    return int(''.join(fakesum), 2)

print("n=3, s=4")
possible = [[4,0,0],
            [3,1,0],
            [2,2,0],
            [2,1,1]
            ]
print(possible)
print([check(n) for n in possible])
