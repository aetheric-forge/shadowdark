# Minimal Textual app: press 'r' to roll, '?' to toggle rule explain
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal
from textual.reactive import reactive

from .core.models import RollRequest
from .core.engine import apply_rules
from .tui.rules_explain_panel import RulesExplainPanel

class RollView(Static):
    last_result = reactive(None)

    def on_mount(self):
        self.update("Press 'r' to roll d20 with advantage. Press '?' to toggle Explain panel.")

    def roll(self):
        req = RollRequest(base_die=20, advantage=True, tags=["demo"])
        res = apply_rules(req)
        self.last_result = res
        rules = ", ".join(r.id for r in res.applied_rules) or "(none)"
        self.update(f"Result: {res.total}  detail={res.detail}  rules=[{rules}]")
        self.post_message(self.ResultChanged(res))

    class ResultChanged(Static.Message):
        def __init__(self, result):
            self.result = result
            super().__init__()

class ShadowdarkApp(App):
    CSS = """
    Screen { layout: horizontal; }
    RulesExplainPanel { width: 1fr; border: wide; }
    RollView { width: 2fr; border: wide; }
    """

    show_explain = reactive(True)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            self.roll_view = RollView()
            yield self.roll_view
            self.explain = RulesExplainPanel()
            yield self.explain
        yield Footer()

    def on_mount(self):
        self.bind("r", "roll", "Roll")
        self.bind("?", "toggle_explain", "Explain")

    def action_roll(self):
        self.roll_view.roll()

    def action_toggle_explain(self):
        self.show_explain = not self.show_explain
        self.explain.display = self.show_explain

    def on_roll_view_result_changed(self, message: RollView.ResultChanged):
        self.explain.show_rules(message.result.applied_rules)

if __name__ == "__main__":
    ShadowdarkApp().run()
