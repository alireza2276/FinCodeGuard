import json

from fincodeguard.experiments.models import ExperimentCondition, ExperimentRun
from fincodeguard.experiments.storage import save_experiment_run
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def test_save_experiment_run(tmp_path) -> None:
    report = VerificationReport(
        task_id="task_001",
        findings=(
            VerificationFinding(
                "SEC-001",
                VerificationCategory.SECURITY,
                VerificationStatus.PASS,
                "Passed.",
            ),
        ),
    )
    run = ExperimentRun(
        "run_001",
        "task_001",
        ExperimentCondition.STANDARD,
        "scripted",
        report,
        report,
    )

    output = save_experiment_run(run, tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["run_id"] == "run_001"
    assert payload["condition"] == "standard"
    assert payload["final_report"]["passed"] is True
