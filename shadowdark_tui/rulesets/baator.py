from __future__ import annotations
from ..models import RollResult
from ..dice import roll


class BaatorRuleset:
    id = "baator"
    name = "Baator"

    # Placeholder: tune mechanics later (edges, corruption, eldritch bursts, etc.)
    def ability_mod(self, score: int) -> int:
        return (score - 10) // 2

    def roll_ability_check(self, ability: str, bonus: int = 0) -> RollResult:
        r = roll("d20")
        r.total += bonus
        r.tags = ["baator", "ability", ability]

    return r

    def roll_attack(self, attack_bonus: int, damage: str):
        return roll(f"d20+{attack_bonus}"), roll(damage)

    def roll_initiative(self, bonus: int = 0) -> RollResult:
        return roll(f"d20+{bonus}")
