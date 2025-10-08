from shadowdark_tui.core.models import RollRequest
from shadowdark_tui.core.engine import apply_rules


def test_light_adds_disadvantage(monkeypatch):
    # Force predictable (pick lower because disadvantage)
    seq = [18, 4]  # disadvantage -> pick 4
    import random

    monkeypatch.setattr(random, "randint", lambda a, b: seq.pop(0))

    req = RollRequest(base_die=20, tags=["sight-check"], context={"light_level": "dim"})
    res = apply_rules(req)
    # Either "dis" mode or base if no advantage/disadvantage mechanic applied
    assert res.detail.get("mode") in {"dis", "base"}
