from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import VerificationReport


@dataclass(frozen=True, slots=True)
class AgentResponse:
    content: str
    model_id: str
    metadata: dict[str, str]


class CodingAgent(ABC):
    @abstractmethod
    def generate(self, task: TaskSpec) -> AgentResponse:
        """Generate an implementation or patch for a task."""

    @abstractmethod
    def repair(
        self,
        task: TaskSpec,
        previous: AgentResponse,
        report: VerificationReport,
    ) -> AgentResponse:
        """Generate a repair using structured verification feedback."""
