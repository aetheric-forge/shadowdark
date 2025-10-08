from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass(frozen=True)
class RuleRef:
    id: str
    reason: Optional[str] = None  # e.g., "advantage flag true", "dim light"

@dataclass
class RollRequest:
    base_die: int            # e.g., 20 for d20
    advantage: bool = False
    disadvantage: bool = False
    tags: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RollResult:
    total: int
    detail: Dict[str, Any]
    applied_rules: List[RuleRef] = field(default_factory=list)
