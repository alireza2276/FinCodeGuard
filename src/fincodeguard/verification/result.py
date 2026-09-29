from dataclasses import dataclass
from enum import StrEnum


class VerificationCategory(StrEnum):
    FUNCTIONAL = "functional"
    SECURITY = "security"
    BUSINESS_INVARIANT = "business_invariant"

class VerificationStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"

@dataclass(frozen=True, slots=True)
class VerificationFinding:
    check_id: str
    category: VerificationCategory
    status: VerificationStatus
    message: str

@dataclass(frozen=True, slots=True)
class VerificationReport:
    task_id: str
    findings: tuple[VerificationFinding, ...] = ()

    @property
    def passed(self) -> bool:
        return bool(self.findings) and all(
            finding.status == VerificationStatus.PASS
            for finding in self.findings
        )

    @property
    def failed_count(self) -> int:
        return sum(
            finding.status in {
                VerificationStatus.FAIL,
                VerificationStatus.ERROR,
            }
            for finding in self.findings
        )
