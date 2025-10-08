from __future__ import annotations

from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button, Input, DataTable

from ..storage import GameStore
from ..dice import roll
from .messages import CharacterSelected


class PartyScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = DataTable(id="party_table")
        self._row_to_ix: dict[str, int] = {}

    def compose(self) -> ComposeResult:
        yield Static("Party", classes="title")
        yield self.table

    def on_mount(self) -> None:
        store = GameStore.instance()
        self.table.clear(columns=True)
        self.table.add_columns("Name", "Class", "Lvl", "HP", "AC")
        self._row_to_ix.clear()
        for ix, c in enumerate(store.party):
            row_key = self.table.add_row(c.name, c.cls, c.level, str(c.hp), str(c.ac))
            self._row_to_ix[row_key] = ix
        if self.table.row_count:
            self.table.cursor_coordinate = (0, 0)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        ix = self._row_to_ix.get(event.row_key)
        if ix is None:
            return
        char = GameStore.instance().party[ix]
        self.post_message(CharacterSelected(character=char))


class CharacterScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = Static("Character", classes="title")
        self.body = Static("Select from Party to view details.")

    def compose(self) -> ComposeResult:
        yield self.header
        yield self.body

    def set_character(self, character, ruleset) -> None:
        s = character.stats
        stat_pairs = [
            ("STR", s.strength),
            ("DEX", s.dexterity),
            ("CON", s.constitution),
            ("INT", s.intelligence),
            ("WIS", s.wisdom),
            ("CHA", s.charisma),
        ]
        rows = []
        for label, score in stat_pairs:
            mod = ruleset.ability_mod(score)
            mod_str = f"{mod:+d}"
            rows.append(f"{label:>3}: {score:>2} ({mod_str})")
        inv = ", ".join(character.inventory) if character.inventory else "—"
        text = (
            f"[b]{character.name}[/b]  •  {character.cls}  •  L{character.level}\n"
            f"HP: {character.hp}   AC: {character.ac}\n\n"
            + "\n".join(rows)
            + f"\n\nInventory: {inv}"
        )
        self.body.update(text)


class InitiativeScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = DataTable(id="init_table")

    def compose(self) -> ComposeResult:
        yield Static("Initiative", classes="title")
        yield self.table
        yield Button("Add", id="add-init")

    def on_mount(self) -> None:
        self.table.clear(columns=True)
        self.table.add_columns("Name", "Init", "HP", "Notes")


class DiceScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input = Input(placeholder="e.g., 2d20kh1+3 or d8+2")
        self.output = Static("Ready.")

    def compose(self) -> ComposeResult:
        yield Static("Dice Roller", classes="title")
        yield self.input
        yield self.output

    def on_input_submitted(self, event: Input.Submitted) -> None:
        expr = event.value.strip()
        try:
            result = roll(expr)
            self.output.update(f"{expr} => **{result.total}**  {result.detail}")
        except Exception as e:
            self.output.update(f"Error: {e}")


class LogScreen(Widget):
    def compose(self) -> ComposeResult:
        yield Static("GM Log (WIP)")
