from __future__ import annotations

from collections.abc import Callable
from uuid import uuid4

from fincodeguard.agents.base import AgentResponse, CodingAgent
from fincodeguard.experiments.models import ExperimentCondition, ExperimentRun
from fincodeguard.experiments.repair import run_repair_loop
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import VerificationReport

VerifierCallback = Callable[[AgentResponse], VerificationReport]


class ExperimentRunner:
    def run(
        self,
        task: TaskSpec,
        agent: CodingAgent,
        verify: VerifierCallback,
        condition: ExperimentCondition,
        max_repairs: int = 2,
    ) -> ExperimentRun:
        if condition == ExperimentCondition.VERIFICATION_GUIDED:
            repair_run = run_repair_loop(
                task=task,
                agent=agent,
                verify=verify,
                max_repairs=max_repairs,
            )
            first = repair_run.iterations[0]
            last = repair_run.iterations[-1]
            return ExperimentRun(
                run_id=str(uuid4()),
                task_id=task.task_id,
                condition=condition,
                model_id=first.response.model_id,
                initial_report=first.report,
                final_report=last.report,
                repair_attempts=max(0, len(repair_run.iterations) - 1),
            )

        response = agent.generate(task)
        report = verify(response)
        return ExperimentRun(
            run_id=str(uuid4()),
            task_id=task.task_id,
            condition=condition,
            model_id=response.model_id,
            initial_report=report,
            final_report=report,
            repair_attempts=0,
        )
