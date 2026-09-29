from fincodeguard.agents.base import AgentResponse
from fincodeguard.agents.scripted import ScriptedAgent
from fincodeguard.experiments.repair import run_repair_loop
from fincodeguard.tasks.schema import TaskSpec
from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


def make_task() -> TaskSpec:
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


def verifier(response: AgentResponse) -> VerificationReport:
    passed = response.content == "fixed"
    return VerificationReport(
        task_id="task_001",
        findings=(
            VerificationFinding(
                check_id="TEST",
                category=VerificationCategory.SECURITY,
                status=VerificationStatus.PASS if passed else VerificationStatus.FAIL,
                message="Synthetic verifier result.",
            ),
        ),
    )


def test_repair_loop_repairs_failed_generation() -> None:
    agent = ScriptedAgent(["broken", "fixed"])
    run = run_repair_loop(make_task(), agent, verifier, max_repairs=2)

    assert run.succeeded is True
    assert len(run.iterations) == 2
    assert run.iterations[0].report.passed is False
    assert run.iterations[1].report.passed is True


def test_repair_loop_stops_when_first_generation_passes() -> None:
    agent = ScriptedAgent(["fixed"])
    run = run_repair_loop(make_task(), agent, verifier, max_repairs=2)

    assert run.succeeded is True
    assert len(run.iterations) == 1
