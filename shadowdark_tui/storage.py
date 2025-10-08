from __future__ import annotations
from pathlib import Path
import yaml
from .models import Character

_DATA = None


class GameStore:
    _instance = None

    def __init__(self, path: str | None = None):
        root = Path(__file__).resolve().parent
        default_path = root / "sample" / "party.yaml"
        self.path = Path(path) if path else default_path
        self.party = self.load_party(self.path)
        GameStore._instance = self

    @staticmethod
    def instance() -> "GameStore":
        return GameStore._instance

    def load_party(self, path: Path):
        data = yaml.safe_load(path.read_text())
        return [Character(**c) for c in data["party"]]
