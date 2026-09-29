from collections.abc import Iterable
from pathlib import Path

from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.base import Verifier
from fincodeguard.verification.result import VerificationFinding, VerificationReport


class VerificationEngine:
    def __init__(self, verifiers: Iterable[Verifier] = ()) -> None:
        self._verifiers = tuple(verifiers)

    def verify(self, task: TaskSpec, candidate_path: str | Path) -> VerificationReport:
        path = Path(candidate_path)
        if not path.exists():
            raise FileNotFoundError(f"Candidate path does not exist: {path}")
        findings: list[VerificationFinding] = []
        for verifier in self._verifiers:
            findings.extend(verifier.verify(task, path))
        return VerificationReport(task.task_id, tuple(findings))
