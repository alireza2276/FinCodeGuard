from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from fincodeguard.experiments.end_to_end import run_pilot_candidate


@dataclass(frozen=True, slots=True)
class PilotTaskResult:
    task_id: str
    candidate: str
    passed: bool
    findings: int
    failed_findings: int


@dataclass(frozen=True, slots=True)
class PilotSummary:
    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    pass_rate: float
    results: tuple[PilotTaskResult, ...]


def discover_candidate(
    candidates_directory: str | Path,
    task_directory: str | Path,
) -> Path:
    candidates = Path(candidates_directory)
    task = Path(task_directory)
    candidate = candidates / f"{task.name}.py"

    if not candidate.is_file():
        raise FileNotFoundError(
            f"Candidate does not exist for {task.name}: {candidate}"
        )
    return candidate


def run_pilot_suite(
    benchmark_directory: str | Path,
    candidates_directory: str | Path,
) -> PilotSummary:
    benchmark = Path(benchmark_directory)
    candidates = Path(candidates_directory)

    task_directories = tuple(
        sorted(
            path
            for path in benchmark.glob("task_*")
            if path.is_dir()
        )
    )
    if not task_directories:
        raise ValueError(
            f"No pilot task directories found in: {benchmark}"
        )

    results = []
    for task_directory in task_directories:
        candidate = discover_candidate(
            candidates,
            task_directory,
        )
        execution = run_pilot_candidate(
            task_directory,
            candidate,
        )
        results.append(
            PilotTaskResult(
                task_id=execution.task_id,
                candidate=str(candidate),
                passed=execution.passed,
                findings=len(execution.report.findings),
                failed_findings=execution.report.failed_count,
            )
        )

    frozen_results = tuple(results)
    passed = sum(result.passed for result in frozen_results)
    total = len(frozen_results)

    return PilotSummary(
        total_tasks=total,
        passed_tasks=passed,
        failed_tasks=total - passed,
        pass_rate=passed / total,
        results=frozen_results,
    )


def write_pilot_summary(
    summary: PilotSummary,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            asdict(summary),
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return path
