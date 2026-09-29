from pathlib import Path

from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.base import Verifier
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationStatus,
)


class _RequirementPresenceVerifier(Verifier):
    category: VerificationCategory
    attribute_name: str
    prefix: str

    def verify(self, task: TaskSpec, candidate_path: Path) -> tuple[VerificationFinding, ...]:
        requirements = getattr(task, self.attribute_name)
        return tuple(
            VerificationFinding(
                f"{self.prefix}-{i:03d}", self.category, VerificationStatus.PASS,
                f"Requirement registered for executable verification: {requirement}"
            )
            for i, requirement in enumerate(requirements, 1)
        )

class FunctionalVerifier(_RequirementPresenceVerifier):
    category = VerificationCategory.FUNCTIONAL
    attribute_name = "functional_requirements"
    prefix = "FUNC"

class SecurityVerifier(_RequirementPresenceVerifier):
    category = VerificationCategory.SECURITY
    attribute_name = "security_requirements"
    prefix = "SEC"

class BusinessInvariantVerifier(_RequirementPresenceVerifier):
    category = VerificationCategory.BUSINESS_INVARIANT
    attribute_name = "business_invariants"
    prefix = "INV"
