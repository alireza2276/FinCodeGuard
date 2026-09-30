from pathlib import Path

from fincodeguard.cli import main

TASK_DIRECTORY = (
    Path("benchmark")
    / "pilot"
    / "task_001_maker_checker"
)


def test_cli_returns_zero_for_passing_candidate(
    tmp_path: Path,
    capsys,
) -> None:
    candidate = tmp_path / "candidate.py"
    candidate.write_text(
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

    exit_code = main(
        [
            str(TASK_DIRECTORY),
            str(candidate),
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Overall: PASS" in captured.out


def test_cli_writes_json_report(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate.py"
    candidate.write_text(
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
    report_path = tmp_path / "report.json"

    exit_code = main(
        [
            str(TASK_DIRECTORY),
            str(candidate),
            "--json-report",
            str(report_path),
        ]
    )

    assert exit_code == 0
    assert report_path.is_file()
