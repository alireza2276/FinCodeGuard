from abc import ABC, abstractmethod
from pathlib import Path

from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import VerificationFinding


class Verifier(ABC):
    @abstractmethod
    def verify(self, task: TaskSpec, candidate_path: Path) -> tuple[VerificationFinding, ...]:
        """Return structured verification findings."""
