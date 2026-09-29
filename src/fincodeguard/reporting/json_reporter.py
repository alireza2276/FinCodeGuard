from __future__ import annotations

import json
from pathlib import Path

from fincodeguard.verification.result import VerificationReport


def report_to_dict(report: VerificationReport) -> dict:
    return {
        "task_id": report.task_id,
        "passed": report.passed,
        "failed_count": report.failed_count,
        "findings": [
            {
                "check_id": finding.check_id,
                "category": finding.category.value,
                "status": finding.status.value,
                "message": finding.message,
            }
            for finding in report.findings
        ],
    }


def write_json_report(report: VerificationReport, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report_to_dict(report), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path
