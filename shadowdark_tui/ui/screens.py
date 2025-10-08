from __future__ import annotations

from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, DataTable

from ..storage import GameStore
from ..dice import roll
from .messages import CharacterSelected, AbilityRolled


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
        t = self.table
        t.clear(columns=True)
        t.add_columns("Name", "Class", "Lvl", "HP", "AC")
        t.cursor_type = "row"
        t.show_cursor = True
        self._row_to_ix.clear()
        for ix, c in enumerate(store.party):
            row_key = t.add_row(c.name, c.cls, c.level, str(c.hp), str(c.ac))
            self._row_to_ix[row_key] = ix
        if t.row_count:
            t.cursor_coordinate = (0, 0)

    def on_data_table_row_activated(self, event: DataTable.RowActivated) -> None:
        self._emit_character(event.row_key)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._emit_character(event.row_key)

    def _emit_character(self, row_key) -> None:
        ix = self._row_to_ix.get(row_key)
        if ix is None:
            return
        char = GameStore.instance().party[ix]
        self.post_message(CharacterSelected(character=char))


class CharacterScreen(Widget):
    can_focus = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = Static("Character", classes="title")
        self.body = Static("Select from Party to view details.")
        self._character = None
        self._ruleset = None

    def compose(self) -> ComposeResult:
        yield self.header
        yield self.body

    def set_character(self, character, ruleset) -> None:
        self._character = character
        self._ruleset = ruleset
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
            rows.append(f"{label:>3}: {score:>2} ({mod:+d})")
        inv = ", ".join(character.inventory) if character.inventory else "—"
        hint = "\n[dim]Keys: 1–6 roll STR/DEX/CON/INT/WIS/CHA • r = reroll last • ? = help[/dim]"
        text = (
            f"[b]{character.name}[/b]  •  {character.cls}  •  L{character.level}\n"
            f"HP: {character.hp}   AC: {character.ac}\n\n"
            + "\n".join(rows)
            + f"\n\nInventory: {inv}"
            + hint
        )
        self.body.update(text)

    # Keyboard-driven ability checks
    def on_key(self, event) -> None:
        if not self._character or not self._ruleset:
            return
        keys = {
            "1": "STR",
            "2": "DEX",
            "3": "CON",
            "4": "INT",
            "5": "WIS",
            "6": "CHA",
            "s": "STR",
            "d": "DEX",
            "c": "CON",
            "i": "INT",
            "w": "WIS",
            "h": "CHA",
        }
        key = getattr(event, "key", None)
        if key in keys:
            ability = keys[key]
            score = getattr(
                self._character.stats,
                {
                    "STR": "strength",
                    "DEX": "dexterity",
                    "CON": "constitution",
                    "INT": "intelligence",
                    "WIS": "wisdom",
                    "CHA": "charisma",
                }[ability],
            )
            mod = self._ruleset.ability_mod(score)
            result = self._ruleset.roll_ability_check(ability, bonus=mod)
            self.post_message(
                AbilityRolled(
                    self._character.name, ability, result.total, result.detail
                )
            )
        elif key == "?":
            self.app.notify(
                "1–6 or s/d/c/i/w/h to roll abilities; 'r' to reroll last (coming soon)"
            )


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

    def show(self, text: str) -> None:
        self.output.update(text)

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
