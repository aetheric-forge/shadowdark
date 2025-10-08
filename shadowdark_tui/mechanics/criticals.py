from ..core.models import RollRequest, RollResult, RuleRef
from ..core import registry

CRIT_RULE = RuleRef(id="SD-CRIT-002")

@registry.register(phase="post", priority=50, name="criticals")
def mark_criticals(req: RollRequest, res: RollResult) -> RollResult:
    # The advantage mechanic stores the raw d20s in detail; fallback to 'total' if absent.
    picked = res.detail.get("picked", res.total)
    if picked == 20:
        res.detail["critical"] = True
        res.applied_rules.append(CRIT_RULE)
    elif picked == 1:
        res.detail["fumble"] = True
        res.applied_rules.append(CRIT_RULE)
    return res

