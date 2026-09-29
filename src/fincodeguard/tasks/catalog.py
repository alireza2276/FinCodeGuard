from __future__ import annotations

from pathlib import Path

from fincodeguard.tasks.loader import load_task
from fincodeguard.tasks.schema import TaskSpec


def discover_tasks(benchmark_root: str | Path) -> tuple[TaskSpec, ...]:
    root = Path(benchmark_root)
    if not root.exists():
        raise FileNotFoundError(f"Benchmark root does not exist: {root}")

    specifications = sorted(root.glob("**/specification.yaml"))
    return tuple(load_task(path) for path in specifications)
