from __future__ import annotations

from fincodeguard.verification.result import VerificationReport


def render_text_report(report: VerificationReport) -> str:
    lines = [
        f"Task: {report.task_id}",
        f"Overall: {'PASS' if report.passed else 'FAIL'}",
        "",
    ]

    for finding in report.findings:
        lines.append(
            
                f"[{finding.status.value.upper()}] "
                f"{finding.check_id} "
                f"({finding.category.value}): "
                f"{finding.message}"
            
        )

    return "\n".join(lines)
