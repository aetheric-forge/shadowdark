from shadowdark_tui.core.models import RollRequest
from shadowdark_tui.core.engine import apply_rules


def test_criticals_mark_20_as_critical(monkeypatch):
    # Force d20s to (20, 5) so picked=20 with advantage
    seq = [20, 5]

    def fake_randint(a, b):
        return seq.pop(0) if seq else 10

    import random

    monkeypatch.setattr(random, "randint", fake_randint)

    req = RollRequest(base_die=20, advantage=True, tags=["attack"])
    res = apply_rules(req)
    assert res.detail.get("critical") is True
    assert any(r.id == "SD-CRIT-002" for r in res.applied_rules)
