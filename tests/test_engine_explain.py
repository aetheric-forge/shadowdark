from shadowdark_tui.core.models import RollRequest
from shadowdark_tui.core.engine import apply_rules

def test_advantage_applies_rule_id(monkeypatch):
    # Make rolls deterministic
    import random
    monkeypatch.setattr(random, "randint", lambda a, b: 10 if a == 1 and b == 20 else 10)

    req = RollRequest(base_die=20, advantage=True, tags=["test"])
    res = apply_rules(req)
    assert res.detail["mode"] == "adv"
    assert any(r.id == "SD-ADV-001" for r in res.applied_rules)
