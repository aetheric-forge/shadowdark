from ..core.models import RollRequest, RuleRef
from ..core import registry

LIGHT_RULE = RuleRef(id="SD-LIGHT-003", reason="dim/low light")


@registry.register(phase="pre", priority=10, name="light")
def apply_light_disadvantage(req: RollRequest) -> RollRequest:
    # Convention: context["light_level"] in {"bright","dim","dark"}
    # and sight-based checks include tag "sight-check"
    lvl = (req.context or {}).get("light_level")
    tags = set(req.tags or [])
    if lvl in {"dim", "dark"} and "sight-check" in tags:
        # set disadvantage unless already at advantage and you choose cancel-out logic elsewhere
        # Keep it simple: flag disadvantage; advantage/disadvantage cancel in the roll mechanic
        req = RollRequest(
            base_die=req.base_die,
            advantage=req.advantage,
            disadvantage=True or req.disadvantage,
            tags=list(tags),
            context=dict(req.context or {}),
        )
        # We can't attach RuleRef at pre stage to the result yet,
        # but we can annotate the reason so downstream UIs can show provenance.
        req.context["_pre_rules"] = req.context.get("_pre_rules", []) + [LIGHT_RULE.id]
    return req
