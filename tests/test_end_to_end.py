from pathlib import Path

from fincodeguard.experiments.end_to_end import run_pilot_candidate
from fincodeguard.verification.result import VerificationCategory

TASK_DIRECTORY = (
    Path("benchmark")
    / "pilot"
    / "task_001_maker_checker"
)


def _write_candidate(
    path: Path,
    secure: bool,
) -> None:
    if secure:
        source = """
def create_payment(maker_id, amount):
    return {
        "maker_id": maker_id,
        "amount": amount,
        "status": "pending",
    }


def approve_payment(payment, actor_id, role):
    if role != "checker":
        raise PermissionError
    if actor_id == payment["maker_id"]:
        raise PermissionError
    payment["status"] = "approved"
"""
    else:
        source = """
def create_payment(maker_id, amount):
    return {
        "maker_id": maker_id,
        "amount": amount,
        "status": "pending",
    }


def approve_payment(payment, actor_id, role):
    payment["status"] = "approved"
"""

    path.write_text(
        source.strip(),
        encoding="utf-8",
    )


def test_end_to_end_accepts_correct_candidate(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "good.py"
    _write_candidate(candidate, secure=True)

    result = run_pilot_candidate(
        TASK_DIRECTORY,
        candidate,
    )

    assert result.passed is True
    assert len(result.report.findings) == 3


def test_end_to_end_exposes_layered_failures(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "bad.py"
    _write_candidate(candidate, secure=False)

    result = run_pilot_candidate(
        TASK_DIRECTORY,
        candidate,
    )

    assert result.passed is False

    failures = {
        finding.category
        for finding in result.report.findings
        if finding.status.value == "fail"
    }

    assert VerificationCategory.SECURITY in failures
    assert VerificationCategory.BUSINESS_INVARIANT in failures
