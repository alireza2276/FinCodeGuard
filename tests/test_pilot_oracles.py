from pathlib import Path

import pytest

from fincodeguard.verification.oracle import run_python_oracle

ROOT = Path("benchmark") / "pilot"
TASKS = [
    "task_001_maker_checker",
    "task_002_duplicate_payment",
    "task_003_approved_immutability",
    "task_004_state_transition",
    "task_005_atomic_transfer",
    "task_006_concurrent_withdrawal",
    "task_007_audit_approval",
    "task_008_sensitive_logging",
]


@pytest.mark.parametrize("task_id", TASKS)
def test_oracles_reject_missing_candidate_api(
    tmp_path: Path,
    task_id: str,
) -> None:
    candidate = tmp_path / f"{task_id}.py"
    candidate.write_text(
        "# intentionally incomplete candidate\n",
        encoding="utf-8",
    )

    report = run_python_oracle(
        task_id,
        ROOT / task_id / "oracle.py",
        candidate,
    )

    assert report.passed is False
    assert report.findings[0].check_id == "ORACLE-ERROR"


def test_maker_checker_distinguishes_bad_and_good(
    tmp_path: Path,
) -> None:
    oracle = (
        ROOT
        / "task_001_maker_checker"
        / "oracle.py"
    )

    bad = tmp_path / "bad.py"
    bad.write_text(
        """
def create_payment(maker_id, amount):
    return {
        "maker_id": maker_id,
        "amount": amount,
        "status": "pending",
    }


def approve_payment(payment, actor_id, role):
    payment["status"] = "approved"
""".strip(),
        encoding="utf-8",
    )

    good = tmp_path / "good.py"
    good.write_text(
        """
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
""".strip(),
        encoding="utf-8",
    )

    bad_report = run_python_oracle(
        "task_001",
        oracle,
        bad,
    )
    good_report = run_python_oracle(
        "task_001",
        oracle,
        good,
    )

    assert bad_report.passed is False
    assert good_report.passed is True
    assert len(good_report.findings) == 3
