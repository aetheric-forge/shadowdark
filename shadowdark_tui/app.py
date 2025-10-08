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
from .ui.messages import CharacterSelected, AbilityRolled


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
        with Horizontal(id="content"):
            yield PartyScreen(id="party_screen")
            with Vertical(id="main-panel"):
                yield CharacterScreen(id="char_screen")
                yield InitiativeScreen(id="init_screen")
                yield DiceScreen(id="dice_screen")
                yield LogScreen(id="log_screen")
        yield Footer()

    def on_mount(self) -> None:
        self.show_only("char_screen")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        tid = event.tab.id
        mapping = {
            "party": "char_screen",
            "char": "char_screen",
            "init": "init_screen",
            "dice": "dice_screen",
            "log": "log_screen",
        }
        self.show_only(mapping.get(tid, "char_screen"))

    def show_only(self, widget_id: str):
        for wid in ("char_screen", "init_screen", "dice_screen", "log_screen"):
            self.query_one(f"#{wid}").display = wid == widget_id

    # Character selection -> populate character sheet & switch to Character
    def on_character_selected(self, msg: CharacterSelected) -> None:
        sheet = self.query_one("#char_screen", expect_type=CharacterScreen)
        sheet.set_character(msg.character, self.ruleset)
        tabs = self.query_one("#tabs", expect_type=Tabs)
        tabs.active = "char"
        self.show_only("char_screen")
        # put focus on the sheet for hotkeys
        sheet.focus()

    # Ability rolled -> show in Dice tab and notify
    def on_ability_rolled(self, msg: AbilityRolled) -> None:
        dice = self.query_one("#dice_screen", expect_type=DiceScreen)
        dice.show(
            f"{msg.character_name} {msg.ability} check => **{msg.total}**  {msg.detail}"
        )
        tabs = self.query_one("#tabs", expect_type=Tabs)
        tabs.active = "dice"
        self.show_only("dice_screen")
        self.notify(f"{msg.character_name} {msg.ability} ⇒ {msg.total}")
