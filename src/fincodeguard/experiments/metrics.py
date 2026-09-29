from __future__ import annotations

from dataclasses import dataclass

from fincodeguard.experiments.models import ExperimentRun
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationStatus,
)


@dataclass(frozen=True, slots=True)
class ExperimentMetrics:
    total_runs: int
    functional_pass_rate: float
    security_pass_rate: float
    business_invariant_pass_rate: float
    fully_correct_rate: float
    repair_success_rate: float
    regression_rate: float


def _category_passed(run: ExperimentRun, category: VerificationCategory) -> bool:
    findings = tuple(
        finding
        for finding in run.final_report.findings
        if finding.category == category
    )
    return bool(findings) and all(
        finding.status == VerificationStatus.PASS for finding in findings
    )


def calculate_metrics(runs: tuple[ExperimentRun, ...]) -> ExperimentMetrics:
    if not runs:
        return ExperimentMetrics(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    total = len(runs)
    functional = sum(
        _category_passed(run, VerificationCategory.FUNCTIONAL) for run in runs
    )
    security = sum(
        _category_passed(run, VerificationCategory.SECURITY) for run in runs
    )
    invariants = sum(
        _category_passed(run, VerificationCategory.BUSINESS_INVARIANT)
        for run in runs
    )
    fully_correct = sum(run.finally_passed for run in runs)

    repair_candidates = tuple(
        run for run in runs if not run.initially_passed and run.repair_attempts > 0
    )
    repaired = sum(run.repaired_successfully for run in repair_candidates)
    repair_rate = repaired / len(repair_candidates) if repair_candidates else 0.0

    regressions = sum(
        run.initially_passed and not run.finally_passed for run in runs
    )

    return ExperimentMetrics(
        total_runs=total,
        functional_pass_rate=functional / total,
        security_pass_rate=security / total,
        business_invariant_pass_rate=invariants / total,
        fully_correct_rate=fully_correct / total,
        repair_success_rate=repair_rate,
        regression_rate=regressions / total,
    )
