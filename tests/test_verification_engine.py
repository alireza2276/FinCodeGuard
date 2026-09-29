from pathlib import Path

from fincodeguard.core.engine import VerificationEngine
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.base import Verifier
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationStatus,
)


class PassingVerifier(Verifier):
    def verify(self, task: TaskSpec, candidate_path: Path):
        return (VerificationFinding("TEST-001", VerificationCategory.FUNCTIONAL,
                                    VerificationStatus.PASS, "Passed."),)

def task():
    return TaskSpec.from_dict({"task_id":"task_001","title":"Example","description":"Example.",
        "functional_requirements":["F"],"security_requirements":["S"],"business_invariants":["I"]})

def test_engine_collects_findings(tmp_path: Path):
    report=VerificationEngine([PassingVerifier()]).verify(task(), tmp_path)
    assert report.passed
    assert report.failed_count == 0
