from ..core.models import RollRequest, RollResult, RuleRef
from ..core.dice import roll_two_d20_pick
from ..core import registry

ADV_RULE = RuleRef(id="SD-ADV-001")


@registry.register(phase="roll", priority=100, name="advantage")
def apply_advantage(req: RollRequest):
    if req.base_die != 20:
        return None
    if req.advantage == req.disadvantage:
        return None
    r1, r2, pick = roll_two_d20_pick(advantage=req.advantage)
    mode = "adv" if req.advantage else "dis"
    return RollResult(
        total=pick,
        detail={"r1": r1, "r2": r2, "picked": pick, "mode": mode},
        applied_rules=[ADV_RULE],
    )
