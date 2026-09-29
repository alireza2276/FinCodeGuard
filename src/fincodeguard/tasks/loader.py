from pathlib import Path
from typing import Any

import yaml

from fincodeguard.tasks.schema import TaskSpec, TaskValidationError


class TaskLoadError(ValueError):
    pass

def load_task(path: str | Path) -> TaskSpec:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise TaskLoadError(f"Task file does not exist: {p}")
    if p.suffix.lower() not in {".yaml", ".yml"}:
        raise TaskLoadError("Task specification must be a YAML file.")
    try:
        raw: Any = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise TaskLoadError(f"Could not load task file: {p}") from exc
    if not isinstance(raw, dict):
        raise TaskLoadError("Task YAML root must be a mapping.")
    try:
        return TaskSpec.from_dict(raw)
    except TaskValidationError as exc:
        raise TaskLoadError(f"Invalid task specification: {exc}") from exc
