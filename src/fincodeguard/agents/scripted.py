from __future__ import annotations

from collections.abc import Iterable

from fincodeguard.agents.base import AgentResponse, CodingAgent
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import VerificationReport


class ScriptedAgent(CodingAgent):
    """Deterministic agent used for tests and reproducible pipeline development."""

    def __init__(self, responses: Iterable[str], model_id: str = "scripted-test-agent") -> None:
        self._responses = iter(responses)
        self._model_id = model_id

    def _next(self) -> AgentResponse:
        try:
            content = next(self._responses)
        except StopIteration as exc:
            raise RuntimeError("ScriptedAgent has no responses remaining.") from exc
        return AgentResponse(content=content, model_id=self._model_id, metadata={})

    def generate(self, task: TaskSpec) -> AgentResponse:
        return self._next()

    def repair(
        self,
        task: TaskSpec,
        previous: AgentResponse,
        report: VerificationReport,
    ) -> AgentResponse:
        return self._next()
