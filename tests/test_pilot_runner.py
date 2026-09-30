from pathlib import Path

import pytest

from fincodeguard.experiments.pilot import (
    discover_candidate,
    write_pilot_summary,
)


def test_discover_candidate_uses_task_directory_name(
    tmp_path: Path,
) -> None:
    task = tmp_path / "task_001_example"
    task.mkdir()

    candidates = tmp_path / "candidates"
    candidates.mkdir()

    candidate = candidates / "task_001_example.py"
    candidate.write_text(
        "# candidate",
        encoding="utf-8",
    )

    assert discover_candidate(candidates, task) == candidate


def test_discover_candidate_rejects_missing_candidate(
    tmp_path: Path,
) -> None:
    task = tmp_path / "task_001_example"
    task.mkdir()

    candidates = tmp_path / "candidates"
    candidates.mkdir()

    with pytest.raises(FileNotFoundError):
        discover_candidate(candidates, task)


def test_write_pilot_summary_creates_json(
    tmp_path: Path,
) -> None:
    from fincodeguard.experiments.pilot import PilotSummary

    summary = PilotSummary(
        total_tasks=0,
        passed_tasks=0,
        failed_tasks=0,
        pass_rate=0.0,
        results=(),
    )

    output = write_pilot_summary(
        summary,
        tmp_path / "summary.json",
    )

    assert output.is_file()
    assert '"total_tasks": 0' in output.read_text(
        encoding="utf-8",
    )
