from fincodeguard.agents.base import AgentResponse
from fincodeguard.agents.scripted import ScriptedAgent
from fincodeguard.experiments.models import ExperimentCondition
from fincodeguard.experiments.runner import ExperimentRunner
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def task() -> TaskSpec:
    return TaskSpec.from_dict(
        {
            "task_id": "task_001",
            "title": "Example",
            "description": "Example task.",
            "functional_requirements": ["F"],
            "security_requirements": ["S"],
            "business_invariants": ["I"],
        }
    )


def verify(response: AgentResponse) -> VerificationReport:
    status = (
        VerificationStatus.PASS
        if response.content == "fixed"
        else VerificationStatus.FAIL
    )
    return VerificationReport(
        task_id="task_001",
        findings=(
            VerificationFinding(
                "FUNC",
                VerificationCategory.FUNCTIONAL,
                status,
                "Synthetic result.",
            ),
        ),
    )


def test_standard_condition_runs_once() -> None:
    run = ExperimentRunner().run(
        task(),
        ScriptedAgent(["fixed"]),
        verify,
        ExperimentCondition.STANDARD,
    )
    assert run.finally_passed is True
    assert run.repair_attempts == 0


def test_verification_guided_condition_repairs() -> None:
    run = ExperimentRunner().run(
        task(),
        ScriptedAgent(["broken", "fixed"]),
        verify,
        ExperimentCondition.VERIFICATION_GUIDED,
    )
    assert run.repaired_successfully is True
    assert run.repair_attempts == 1
