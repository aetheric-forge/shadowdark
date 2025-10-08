# Shadowdark TUI — Hybrid Rules + Engine Scaffold

This scaffold demonstrates a hybrid approach where **Markdown rules** are the canonical,
human-readable source and **Python mechanics** are thin, deterministic executors that cite
those rules via stable IDs (`RuleRef`). The TUI can show "Explain" panels live.

## Layout
```
shadowdark_tui/
  app.py                         # Minimal Textual app with a Roll demo + Explain panel
  __init__.py
  core/
    models.py                    # dataclasses for RuleRef, RollRequest, RollResult, etc.
    engine.py                    # rule dispatcher + precedence handling
    registry.py                  # registry for mechanics
    dice.py                      # pure dice utilities (seedable)
  mechanics/
    advantage.py                 # example mechanic that cites SD-ADV-001
  rules/
    mechanics/
      SD-ADV-001.md              # canonical Markdown rule (with YAML front matter)
  tui/
    rules_explain_panel.py       # panel to render Markdown rule summaries
tests/
  test_engine_explain.py         # demonstrates "applied rule IDs" expectation
main.py                          # simple CLI entry point
requirements.txt                 # baseline deps (Textual optional if you just run tests)
```

## Quickstart

- Run tests (no Textual required):
  ```bash
  python -m pytest -q
  ```

- Run the demo TUI (requires `textual` and `rich`):
  ```bash
  pip install -r requirements.txt
  python -m shadowdark_tui.app
  ```

- Try the CLI roll (no TUI):
  ```bash
  python main.py --advantage
  ```

## Philosophy
- The rules Markdown is the **source of truth**; Python references it via `RuleRef.id`.
- Mechanics never hard-code prose. They cite rules.
- The engine returns `(result, applied_rules)` so the UI can "show your work."
- Only automate what DMs repeatedly calculate or frequently misapply.
