import json

from fincodeguard.experiments.evaluation import write_evaluation_summary
from fincodeguard.experiments.models import ExperimentCondition, ExperimentRun
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def test_write_evaluation_summary(tmp_path) -> None:
    report = VerificationReport(
        "task_001",
        (
            VerificationFinding(
                "FUNC",
                VerificationCategory.FUNCTIONAL,
                VerificationStatus.PASS,
                "Passed.",
            ),
            VerificationFinding(
                "SEC",
                VerificationCategory.SECURITY,
                VerificationStatus.PASS,
                "Passed.",
            ),
            VerificationFinding(
                "INV",
                VerificationCategory.BUSINESS_INVARIANT,
                VerificationStatus.PASS,
                "Passed.",
            ),
        ),
    )
    run = ExperimentRun(
        "run_001",
        "task_001",
        ExperimentCondition.STANDARD,
        "model",
        report,
        report,
    )

    output = write_evaluation_summary((run,), tmp_path / "summary.json")
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["total_runs"] == 1
    assert payload["fully_correct_rate"] == 1.0
