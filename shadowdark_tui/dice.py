import random
import re
from .models import RollResult

# Simple dice parser supporting NdM, plus keep-high/keep-low (kh/kl), and +/- modifiers.
DICE_RE = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<keep>(kh|kl)\d+)?(?P<mod>[+-]\d+)?$"
)


def roll(expr: str) -> RollResult:
    m = DICE_RE.match(expr.replace(" ", ""))
    if not m:
        raise ValueError("Bad expression. Try like '2d20kh1+3' or 'd8+2'.")
    count = int(m.group("count") or 1)
    sides = int(m.group("sides"))
    keep = m.group("keep")
    mod = int(m.group("mod") or 0)

    rolls = [random.randint(1, sides) for _ in range(count)]
    kept = rolls
    if keep:
        k = int(keep[2:])
    if keep.startswith("kh"):
        kept = sorted(rolls, reverse=True)[:k]
    else:
        kept = sorted(rolls)[:k]
        total = sum(kept) + mod
        detail = f"rolls={rolls} kept={kept} mod={mod}"
    return RollResult(expression=expr, detail=detail, total=total)
