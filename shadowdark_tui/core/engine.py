from typing import Optional
import importlib
from .models import RollRequest, RollResult
from .dice import roll_die
from . import registry


def apply_rules(req: RollRequest) -> RollResult:
    # Auto-load mechanics (lazy to avoid import-time explosions)
    try:
        importlib.import_module("shadowdark_tui.mechanics")
    except Exception:
        pass

    # PRE phase: transform the request (e.g., set disadvantage from light)
    for e in registry.get_phase("pre"):
        if e.pre_fn:
            req = e.pre_fn(req)

    # ROLL phase: pick the final roll result according to priority order
    result: Optional[RollResult] = None
    for e in registry.get_phase("roll"):
        if e.roll_fn:
            out = e.roll_fn(req)
            if out:
                result = out

    # Fallback if no roll mechanics fired
    if result is None:
        result = RollResult(
            total=roll_die(req.base_die), detail={"mode": "base"}, applied_rules=[]
        )

    # POST phase: annotate/adjust the result (e.g., critical/fumble markers)
    for e in registry.get_phase("post"):
        if e.post_fn:
            result = e.post_fn(req, result)

    return result
