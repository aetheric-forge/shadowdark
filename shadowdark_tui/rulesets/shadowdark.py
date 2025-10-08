from __future__ import annotations
from ..models import RollResult
from ..dice import roll


class ShadowdarkRuleset:
    id = "shadowdark"
    name = "Shadowdark"

    def ability_mod(self, score: int) -> int:
        # B/X-style brackets (simple, table-friendly)
        if score <= 5:
            return -3
        if score <= 8:
            return -1
        if score <= 12:
            return 0
        if score <= 15:
            return +1
        if score <= 17:
            return +2
        return +3

    def roll_ability_check(self, ability: str, bonus: int = 0) -> RollResult:
        r = roll("d20")
        total = r.total + bonus
        return RollResult(
            expression=f"d20+{bonus if bonus else 0}",
            detail=r.detail,
            total=total,
            tags=["ability", ability],
        )

    def roll_attack(
        self, attack_bonus: int, damage: str
    ) -> tuple[RollResult, RollResult]:
        atk = roll(f"d20+{attack_bonus}")
        dmg = roll(damage)
        atk.tags = ["attack"]
        dmg.tags = ["damage"]
        return atk, dmg

    def roll_initiative(self, bonus: int = 0) -> RollResult:
        return roll(f"d20+{bonus}")
