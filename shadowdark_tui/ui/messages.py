from __future__ import annotations
from dataclasses import dataclass
from textual.message import Message


@dataclass
class CharacterSelected(Message):
    character: "Character"  # forward ref; import only where used
