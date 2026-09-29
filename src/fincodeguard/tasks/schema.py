from dataclasses import dataclass, field
from typing import Any


class TaskValidationError(ValueError):
    pass

def _text(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise TaskValidationError(f"{name} must be a non-empty string.")
    return v.strip()

def _items(v: Any, name: str, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(v, list):
        raise TaskValidationError(f"{name} must be a list of strings.")
    out = tuple(_text(x, name) for x in v)
    if not allow_empty and not out:
        raise TaskValidationError(f"{name} must contain at least one item.")
    return out

@dataclass(frozen=True, slots=True)
class TaskSpec:
    task_id: str
    title: str
    description: str
    functional_requirements: tuple[str, ...]
    security_requirements: tuple[str, ...]
    business_invariants: tuple[str, ...]
    preconditions: tuple[str, ...] = ()
    postconditions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskSpec":
        if not isinstance(data, dict):
            raise TaskValidationError("Task specification must be a mapping.")
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict):
            raise TaskValidationError("metadata must be a mapping.")
        return cls(
            _text(data.get("task_id"), "task_id"),
            _text(data.get("title"), "title"),
            _text(data.get("description"), "description"),
            _items(data.get("functional_requirements"), "functional_requirements"),
            _items(data.get("security_requirements"), "security_requirements"),
            _items(data.get("business_invariants"), "business_invariants"),
            _items(data.get("preconditions", []), "preconditions", True),
            _items(data.get("postconditions", []), "postconditions", True),
            dict(metadata),
        )
