from __future__ import annotations

import json
from pathlib import Path

from fincodeguard.experiments.models import ExperimentRun
from fincodeguard.reporting.json_reporter import report_to_dict


def experiment_run_to_dict(run: ExperimentRun) -> dict:
    return {
        "run_id": run.run_id,
        "task_id": run.task_id,
        "condition": run.condition.value,
        "model_id": run.model_id,
        "repair_attempts": run.repair_attempts,
        "initial_report": report_to_dict(run.initial_report),
        "final_report": report_to_dict(run.final_report),
        "metadata": run.metadata,
    }


def save_experiment_run(
    run: ExperimentRun,
    output_directory: str | Path,
) -> Path:
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{run.run_id}.json"
    path.write_text(
        json.dumps(experiment_run_to_dict(run), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path
