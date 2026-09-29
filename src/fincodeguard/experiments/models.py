from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from fincodeguard.verification.result import VerificationReport


class ExperimentCondition(StrEnum):
    STANDARD = "standard"
    SECURITY_AWARE = "security_aware"
    VERIFICATION_GUIDED = "verification_guided"


@dataclass(frozen=True, slots=True)
class ExperimentRun:
    run_id: str
    task_id: str
    condition: ExperimentCondition
    model_id: str
    initial_report: VerificationReport
    final_report: VerificationReport
    repair_attempts: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def initially_passed(self) -> bool:
        return self.initial_report.passed

    @property
    def finally_passed(self) -> bool:
        return self.final_report.passed

    @property
    def repaired_successfully(self) -> bool:
        return (
            not self.initially_passed
            and self.finally_passed
            and self.repair_attempts > 0
        )
