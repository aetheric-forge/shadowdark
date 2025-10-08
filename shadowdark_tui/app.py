# shadowdark_tui/app.py (fix compose + ids)

from __future__ import annotations
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Tabs, Tab
from textual.reactive import reactive
from .ui.screens import (
    PartyScreen,
    CharacterScreen,
    InitiativeScreen,
    DiceScreen,
    LogScreen,
)
from .storage import GameStore
from .rulesets.shadowdark import ShadowdarkRuleset


class ShadowdarkApp(App):
    CSS_PATH = "ui/styles.tcss"
    TITLE = "Shadowdark JIT TUI"

    active_tab = reactive("party")

    def __init__(self):
        super().__init__()
        self.store = GameStore()
        self.ruleset = ShadowdarkRuleset()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Tabs(
            Tab("Party", id="party"),
            Tab("Character", id="char"),
            Tab("Initiative", id="init"),
            Tab("Dice", id="dice"),
            Tab("GM Log", id="log"),
            id="tabs",
        )
        # give the middle row an id so the CSS can target it
        with Horizontal(id="content"):
            yield PartyScreen(id="party_screen")
            with Vertical(id="main-panel"):
                yield CharacterScreen(id="char_screen")
                yield InitiativeScreen(id="init_screen")
                yield DiceScreen(id="dice_screen")
                yield LogScreen(id="log_screen")
        yield Footer()

    def on_mount(self) -> None:
        # show Character by default
        self.show_only("char_screen")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        tid = event.tab.id
        mapping = {
            "party": "char_screen",  # keep left pane (party) always visible; main panel swaps
            "char": "char_screen",
            "init": "init_screen",
            "dice": "dice_screen",
            "log": "log_screen",
        }
        self.show_only(mapping.get(tid, "char_screen"))

    def show_only(self, widget_id: str):
        # Toggle only the main-panel children
        for wid in ("char_screen", "init_screen", "dice_screen", "log_screen"):
            self.query_one(f"#{wid}").display = wid == widget_id

    def on_character_selected(self, msg: CharacterSelected) -> None:
        sheet = self.query_one("#char_screen", expect_type=CharacterScreen)
        sheet.set_character(msg.character, self.ruleset)
        # self.query_one("#tabs").active = "char"  # uncomment if you want auto-swap
