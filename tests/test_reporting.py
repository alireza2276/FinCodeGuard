import json

from fincodeguard.reporting.json_reporter import report_to_dict, write_json_report
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def make_report() -> VerificationReport:
    return VerificationReport(
        task_id="task_001",
        findings=(
            VerificationFinding(
                check_id="SEC-001",
                category=VerificationCategory.SECURITY,
                status=VerificationStatus.FAIL,
                message="Unauthorized approval accepted.",
            ),
        ),
    )


def test_report_to_dict() -> None:
    payload = report_to_dict(make_report())
    assert payload["passed"] is False
    assert payload["failed_count"] == 1
    assert payload["findings"][0]["category"] == "security"


def test_write_json_report(tmp_path) -> None:
    output = write_json_report(make_report(), tmp_path / "report.json")
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["task_id"] == "task_001"
