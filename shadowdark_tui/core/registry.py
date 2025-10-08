from dataclasses import dataclass
from typing import Callable, List, Literal, Optional
from ..core.models import RollRequest, RollResult

Phase = Literal["pre", "roll", "post"]


@dataclass
class _Entry:
    phase: Phase
    priority: int
    pre_fn: Optional[Callable[[RollRequest], RollRequest]] = None
    roll_fn: Optional[Callable[[RollRequest], Optional[RollResult]]] = None
    post_fn: Optional[Callable[[RollRequest, RollResult], RollResult]] = None
    name: str = "mechanic"


_REGISTRY: List[_Entry] = []


def register(*, phase: Phase = "roll", priority: int = 100, name: str = "mechanic"):
    def deco(fn):
        entry = _Entry(phase=phase, priority=priority, name=name)
        if phase == "pre":
            entry.pre_fn = fn
        elif phase == "roll":
            entry.roll_fn = fn
        elif phase == "post":
            entry.post_fn = fn
        else:
            raise ValueError(f"Unknown phase: {phase}")
        _REGISTRY.append(entry)
        return fn

    return deco


def get_phase(phase: Phase) -> List[_Entry]:
    return sorted([e for e in _REGISTRY if e.phase == phase], key=lambda e: e.priority)
