from pathlib import Path

from fincodeguard.tasks.catalog import discover_tasks


def test_pilot_contains_eight_valid_tasks() -> None:
    tasks = discover_tasks(Path("benchmark") / "pilot")
    assert len(tasks) == 8
    assert len({task.task_id for task in tasks}) == 8
    assert all(task.functional_requirements for task in tasks)
    assert all(task.security_requirements for task in tasks)
    assert all(task.business_invariants for task in tasks)
