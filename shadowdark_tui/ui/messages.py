from __future__ import annotations
from textual.message import Message


class CharacterSelected(Message):
    def __init__(self, character) -> None:
        self.character = character
        super().__init__()

    @property
    def bubble(self) -> bool:
        return True


class AbilityRolled(Message):
    """Emitted when the Character screen rolls an ability check."""

    def __init__(
        self, character_name: str, ability: str, total: int, detail: str
    ) -> None:
        self.character_name = character_name
        self.ability = ability
        self.total = total
        self.detail = detail
        super().__init__()

    @property
    def bubble(self) -> bool:
        return True
