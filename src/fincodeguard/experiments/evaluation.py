from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from fincodeguard.experiments.metrics import calculate_metrics
from fincodeguard.experiments.models import ExperimentRun


def write_evaluation_summary(
    runs: tuple[ExperimentRun, ...],
    output_path: str | Path,
) -> Path:
    metrics = calculate_metrics(runs)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(metrics), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path
