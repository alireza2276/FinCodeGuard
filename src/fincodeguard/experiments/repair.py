from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fincodeguard.agents.base import AgentResponse, CodingAgent
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import VerificationReport

VerifierCallback = Callable[[AgentResponse], VerificationReport]


@dataclass(frozen=True, slots=True)
class RepairIteration:
    number: int
    response: AgentResponse
    report: VerificationReport


@dataclass(frozen=True, slots=True)
class RepairRun:
    task_id: str
    iterations: tuple[RepairIteration, ...]

    @property
    def succeeded(self) -> bool:
        return bool(self.iterations) and self.iterations[-1].report.passed


def run_repair_loop(
    task: TaskSpec,
    agent: CodingAgent,
    verify: VerifierCallback,
    max_repairs: int = 2,
) -> RepairRun:
    if max_repairs < 0:
        raise ValueError("max_repairs must be zero or greater.")

    response = agent.generate(task)
    report = verify(response)
    iterations = [RepairIteration(0, response, report)]

    for repair_number in range(1, max_repairs + 1):
        if report.passed:
            break
        response = agent.repair(task, response, report)
        report = verify(response)
        iterations.append(RepairIteration(repair_number, response, report))

    return RepairRun(task_id=task.task_id, iterations=tuple(iterations))
