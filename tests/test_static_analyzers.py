from pathlib import Path
from unittest.mock import patch

from fincodeguard.analyzers.static import BanditAnalyzer, SemgrepAnalyzer
from fincodeguard.verification.result import VerificationStatus


@patch("fincodeguard.analyzers.static.shutil.which", return_value=None)
def test_bandit_missing_tool_returns_error(_mock) -> None:
    result = BanditAnalyzer().analyze(Path("."))
    assert result.findings[0].status == VerificationStatus.ERROR


@patch("fincodeguard.analyzers.static.shutil.which", return_value=None)
def test_semgrep_missing_tool_returns_error(_mock) -> None:
    result = SemgrepAnalyzer().analyze(Path("."))
    assert result.findings[0].status == VerificationStatus.ERROR
