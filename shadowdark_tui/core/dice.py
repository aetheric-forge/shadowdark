import random

def roll_die(sides: int) -> int:
    return random.randint(1, sides)

def roll_two_d20_pick(advantage: bool):
    import random
    r1 = random.randint(1, 20)
    r2 = random.randint(1, 20)
    pick = max(r1, r2) if advantage else min(r1, r2)
    return r1, r2, pick
