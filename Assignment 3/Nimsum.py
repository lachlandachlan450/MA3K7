#Making nim
import random

def nimsum(n): #We want to end our turn on a nimsum=0
    if not n or all(a == 0 for a in n):
        return 0
    binary = [bin(a)[2:] for a in n if a > 0]  # drop zeros cleanly
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


def nim(n):
    turn = True
    while any(a > 0 for a in n):          # FIX: works for any pile count
        if turn:
            print(f"The stick piles are {n}. It's your turn.")
            playermove(n)
            turn = False
        else:
            print(f"The bot moved.")
            botmove(n)
            turn = True

    # In misere, whoever took the last stick LOSES.
    if turn:
        print("The bot picked up the last stick -- bot loses, you win!")
    else:
        print("You picked up the last stick -- you lose, bot wins!")


def playermove(n):
    heap = int(input("What pile would you like to pick up from (0=first pile)"))
    while heap < 0 or heap >= len(n) or n[heap] == 0:   # FIX: reject empty piles
        print("Out of range")
        heap = int(input("What pile would you like to pick up from (0=first pile)"))
    val = int(input("How many sticks would you like to take from the pile"))
    while val < 1 or val > n[heap]:
        print("Out of range")
        val = int(input("How many sticks would you like to take from the pile"))
    n[heap] -= val


def botmove(n):
    bigpiles = [i for i in n if i > 1]
    if len(bigpiles) <= 1:
        botendgame(n)
        return True

    if nimsum(n) == 0:
        # Losing position under normal play; in misere this is also losing
        # while >=2 big piles remain, so just make a legal move.
        a = random.choice([i for i in range(len(n)) if n[i] > 0])
        n[a] -= 1
        return False

    # Search for a move that makes the XOR sum zero.
    for heap in range(len(n)):
        for val in range(1, n[heap] + 1):
            if checkmove(n, heap, val):
                # FIX: misere trap -- if this XOR move would leave <=1 big pile,
                # the endgame rule takes over instead.
                m = n[:]
                m[heap] -= val
                if len([x for x in m if x > 1]) <= 1:
                    botendgame(n)
                    return True
                n[heap] -= val
                return True

    # Should never happen if nimsum != 0, but be safe.
    a = random.choice([i for i in range(len(n)) if n[i] > 0])
    n[a] -= 1
    return False


def botendgame(n):
    piles1 = [i for i in range(len(n)) if n[i] == 1]
    pos = [i for i in range(len(n)) if n[i] > 1]

    if not pos:
        # Only 1-piles (or empty) left.
        if piles1:
            n[piles1[0]] -= 1
        return

    if len(piles1) == 0:
        # One big pile, no 1s: leave opponent a single 1-pile (odd).
        n[pos[0]] = 1
    elif len(piles1) % 2 == 0:
        # Even number of 1s: take one away to make it odd.
        n[piles1[0]] -= 1
    else:
        # Odd number of 1s: take the WHOLE big pile (FIX: was = 1).
        n[pos[0]] = 0


def checkmove(n, heap, val):
    m = [a for a in n]
    m[heap] -= val
    if m[heap] < 0:
        return False
    if nimsum(m) == 0:
        return True
    return False


game1 = [4, 4, 4, 4, 4, 1]

nim(game1)
