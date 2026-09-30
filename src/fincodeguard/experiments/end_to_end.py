from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fincodeguard.tasks.loader import load_task
from fincodeguard.verification.oracle import run_python_oracle
from fincodeguard.verification.result import VerificationReport


@dataclass(frozen=True, slots=True)
class EndToEndResult:
    task_id: str
    task_directory: Path
    candidate_path: Path
    report: VerificationReport

    @property
    def passed(self) -> bool:
        return self.report.passed


def run_pilot_candidate(
    task_directory: str | Path,
    candidate_path: str | Path,
) -> EndToEndResult:
    task_dir = Path(task_directory)
    candidate = Path(candidate_path)

    specification = task_dir / "specification.yaml"
    oracle = task_dir / "oracle.py"

    if not task_dir.is_dir():
        raise FileNotFoundError(
            f"Task directory does not exist: {task_dir}"
        )
    if not specification.is_file():
        raise FileNotFoundError(
            f"Task specification does not exist: {specification}"
        )
    if not oracle.is_file():
        raise FileNotFoundError(
            f"Task oracle does not exist: {oracle}"
        )

    task = load_task(specification)
    report = run_python_oracle(
        task.task_id,
        oracle,
        candidate,
    )

    return EndToEndResult(
        task_id=task.task_id,
        task_directory=task_dir,
        candidate_path=candidate,
        report=report,
    )
