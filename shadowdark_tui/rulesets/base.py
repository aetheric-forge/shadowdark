from __future__ import annotations
from typing import Protocol
from ..models import RollResult
from ..dice import roll


class Ruleset(Protocol):
    id: str
    name: str

    def ability_mod(self, score: int) -> int: ...
    def roll_ability_check(self, ability: str, bonus: int = 0) -> RollResult: ...
    def roll_attack(
        self, attack_bonus: int, damage: str
    ) -> tuple[RollResult, RollResult]: ...
    def roll_initiative(self, bonus: int = 0) -> RollResult: ...
