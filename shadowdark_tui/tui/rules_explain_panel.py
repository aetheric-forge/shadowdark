from textual.widgets import Static
from textual.reactive import reactive
from textual import events
from pathlib import Path

class RulesExplainPanel(Static):
    rule_paths = reactive([])

    def show_rules(self, rule_refs):
        base = Path(__file__).resolve().parents[1] / "rules"
        texts = []
        for ref in rule_refs or []:
            # naive path mapping: mechanics only, extend later
            p = base / "mechanics" / f"{ref.id}.md"
            if p.exists():
                texts.append(p.read_text(encoding="utf-8"))
            else:
                texts.append(f"# {ref.id}\n*(No summary file found yet.)*")
        if not texts:
            texts = ["*No rules applied.*"]
        self.update("\n\n---\n\n".join(texts))
