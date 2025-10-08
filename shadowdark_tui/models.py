from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict


class Stats(BaseModel):
    # internal names are safe; YAML can still use 'str', 'dex', etc.
    model_config = ConfigDict(populate_by_name=True)

    strength: int = Field(10, alias="str")
    dexterity: int = Field(10, alias="dex")
    constitution: int = Field(10, alias="con")
    intelligence: int = Field(10, alias="int")
    wisdom: int = Field(10, alias="wis")
    charisma: int = Field(10, alias="cha")


class Character(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    cls: str = Field(alias="class")
    level: int = 1
    hp: int = 1
    ac: int = 10
    stats: Stats = Stats()
    inventory: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Encounter(BaseModel):
    name: str
    combatants: List[str] = Field(default_factory=list)
    initiative: Dict[str, int] = Field(default_factory=dict)
    round: int = 0
    notes: str = ""


class RollResult(BaseModel):
    expression: str
    detail: str
    total: int
    tags: List[str] = Field(default_factory=list)
