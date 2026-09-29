from pathlib import Path

from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.layers import (
    BusinessInvariantVerifier,
    FunctionalVerifier,
    SecurityVerifier,
)
from fincodeguard.verification.result import VerificationCategory, VerificationStatus


def test_three_layers(tmp_path: Path):
    task=TaskSpec.from_dict({"task_id":"task_001","title":"Example","description":"Example.",
        "functional_requirements":["F"],"security_requirements":["S"],"business_invariants":["I"]})
    findings=(FunctionalVerifier().verify(task,tmp_path)+SecurityVerifier().verify(task,tmp_path)+
              BusinessInvariantVerifier().verify(task,tmp_path))
    assert len(findings)==3
    assert {x.category for x in findings} == {VerificationCategory.FUNCTIONAL,
        VerificationCategory.SECURITY, VerificationCategory.BUSINESS_INVARIANT}
    assert all(x.status == VerificationStatus.PASS for x in findings)
