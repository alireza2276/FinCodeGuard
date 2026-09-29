from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationStatus,
)


@dataclass(frozen=True, slots=True)
class StaticAnalyzerResult:
    analyzer: str
    findings: tuple[VerificationFinding, ...]


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


class BanditAnalyzer:
    """Run Bandit when it is installed and convert results to FinCodeGuard findings."""

    def analyze(self, candidate_path: Path) -> StaticAnalyzerResult:
        executable = shutil.which("bandit")
        if executable is None:
            return StaticAnalyzerResult(
                analyzer="bandit",
                findings=(
                    VerificationFinding(
                        check_id="BANDIT-TOOL",
                        category=VerificationCategory.SECURITY,
                        status=VerificationStatus.ERROR,
                        message="Bandit is not installed in the current environment.",
                    ),
                ),
            )

        result = _run([executable, "-r", ".", "-f", "json", "-q"], candidate_path)
        try:
            payload = json.loads(result.stdout or "{}")
        except json.JSONDecodeError:
            payload = {}

        issues = payload.get("results", [])
        if not issues and result.returncode in {0, 1}:
            return StaticAnalyzerResult(
                analyzer="bandit",
                findings=(
                    VerificationFinding(
                        check_id="BANDIT",
                        category=VerificationCategory.SECURITY,
                        status=VerificationStatus.PASS,
                        message="Bandit reported no security findings.",
                    ),
                ),
            )

        findings = tuple(
            VerificationFinding(
                check_id=f"BANDIT-{issue.get('test_id', 'UNKNOWN')}",
                category=VerificationCategory.SECURITY,
                status=VerificationStatus.FAIL,
                message=issue.get("issue_text", "Bandit security finding."),
            )
            for issue in issues
        )
        if findings:
            return StaticAnalyzerResult("bandit", findings)

        return StaticAnalyzerResult(
            analyzer="bandit",
            findings=(
                VerificationFinding(
                    check_id="BANDIT-ERROR",
                    category=VerificationCategory.SECURITY,
                    status=VerificationStatus.ERROR,
                    message=(result.stderr or "Bandit execution failed.").strip(),
                ),
            ),
        )


class SemgrepAnalyzer:
    """Run Semgrep when installed and convert results to FinCodeGuard findings."""

    def analyze(self, candidate_path: Path) -> StaticAnalyzerResult:
        executable = shutil.which("semgrep")
        if executable is None:
            return StaticAnalyzerResult(
                analyzer="semgrep",
                findings=(
                    VerificationFinding(
                        check_id="SEMGREP-TOOL",
                        category=VerificationCategory.SECURITY,
                        status=VerificationStatus.ERROR,
                        message="Semgrep is not installed in the current environment.",
                    ),
                ),
            )

        result = _run(
            [executable, "scan", "--config", "auto", "--json", "."],
            candidate_path,
        )
        try:
            payload = json.loads(result.stdout or "{}")
        except json.JSONDecodeError:
            payload = {}

        issues = payload.get("results", [])
        if not issues and result.returncode == 0:
            return StaticAnalyzerResult(
                analyzer="semgrep",
                findings=(
                    VerificationFinding(
                        check_id="SEMGREP",
                        category=VerificationCategory.SECURITY,
                        status=VerificationStatus.PASS,
                        message="Semgrep reported no findings.",
                    ),
                ),
            )

        findings = tuple(
            VerificationFinding(
                check_id=f"SEMGREP-{index:03d}",
                category=VerificationCategory.SECURITY,
                status=VerificationStatus.FAIL,
                message=item.get("extra", {}).get("message", "Semgrep finding."),
            )
            for index, item in enumerate(issues, start=1)
        )
        if findings:
            return StaticAnalyzerResult("semgrep", findings)

        return StaticAnalyzerResult(
            analyzer="semgrep",
            findings=(
                VerificationFinding(
                    check_id="SEMGREP-ERROR",
                    category=VerificationCategory.SECURITY,
                    status=VerificationStatus.ERROR,
                    message=(result.stderr or "Semgrep execution failed.").strip(),
                ),
            ),
        )
