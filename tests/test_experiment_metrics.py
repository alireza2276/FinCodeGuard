from fincodeguard.experiments.metrics import calculate_metrics
from fincodeguard.experiments.models import ExperimentCondition, ExperimentRun
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def report(task_id: str, status: VerificationStatus) -> VerificationReport:
    return VerificationReport(
        task_id=task_id,
        findings=tuple(
            VerificationFinding(
                category.value,
                category,
                status,
                "Synthetic result.",
            )
            for category in VerificationCategory
        ),
    )


def test_metrics_are_calculated_from_runs() -> None:
    passing = report("task_1", VerificationStatus.PASS)
    failing = report("task_2", VerificationStatus.FAIL)

    runs = (
        ExperimentRun(
            "run_1",
            "task_1",
            ExperimentCondition.STANDARD,
            "model",
            passing,
            passing,
        ),
        ExperimentRun(
            "run_2",
            "task_2",
            ExperimentCondition.VERIFICATION_GUIDED,
            "model",
            failing,
            passing,
            repair_attempts=1,
        ),
    )

    metrics = calculate_metrics(runs)

    assert metrics.total_runs == 2
    assert metrics.functional_pass_rate == 1.0
    assert metrics.security_pass_rate == 1.0
    assert metrics.business_invariant_pass_rate == 1.0
    assert metrics.fully_correct_rate == 1.0
    assert metrics.repair_success_rate == 1.0
