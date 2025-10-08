import random
import re
from .models import RollResult

# Simple dice parser supporting NdM, keep-high/keep-low (kh/kl), and +/- modifiers.
DICE_RE = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<keep>(kh|kl)\d+)?(?P<mod>[+-]\d+)?$"
)


def roll(expr: str) -> RollResult:
    s = expr.replace(" ", "")
    m = DICE_RE.match(s)
    if not m:
        raise ValueError("Bad expression. Try like '2d20kh1+3' or 'd8+2'.")

    count = int(m.group("count") or 1)
    sides = int(m.group("sides"))
    keep = m.group("keep")  # e.g., 'kh1' / 'kl1' or None
    mod = int(m.group("mod") or 0)

    rolls = [random.randint(1, sides) for _ in range(count)]
    kept = rolls

    if keep is not None:
        k = int(keep[2:])  # digits after kh/kl
        if keep.startswith("kh"):
            kept = sorted(rolls, reverse=True)[:k]
        else:  # 'kl'
            kept = sorted(rolls)[:k]

    total = sum(kept) + mod
    detail = f"rolls={rolls} kept={kept} mod={mod}"
    return RollResult(expression=s, detail=detail, total=total)
