from fincodeguard.reporting.text_reporter import render_text_report
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def test_render_text_report() -> None:
    report = VerificationReport(
        task_id="task_001",
        findings=(
            VerificationFinding(
                "FUNC-001",
                VerificationCategory.FUNCTIONAL,
                VerificationStatus.PASS,
                "Functional check passed.",
            ),
            VerificationFinding(
                "INV-001",
                VerificationCategory.BUSINESS_INVARIANT,
                VerificationStatus.FAIL,
                "Invariant failed.",
            ),
        ),
    )

    output = render_text_report(report)

    assert "Task: task_001" in output
    assert "Overall: FAIL" in output
    assert "[PASS] FUNC-001" in output
    assert "[FAIL] INV-001" in output
