import json
from pathlib import Path

TASK_IDS = (
    "task_001_maker_checker",
    "task_002_duplicate_payment",
    "task_003_approved_immutability",
    "task_004_state_transition",
    "task_005_atomic_transfer",
    "task_006_concurrent_withdrawal",
    "task_007_audit_approval",
    "task_008_sensitive_logging",
)


def test_all_frozen_pilot_prompts_exist() -> None:
    prompt_root = Path("prompts") / "pilot"

    for task_id in TASK_IDS:
        prompt = prompt_root / f"{task_id}.txt"
        assert prompt.is_file()
        content = prompt.read_text(encoding="utf-8")
        assert "Do not assume access to benchmark tests" in content


def test_metadata_template_covers_all_tasks() -> None:
    path = (
        Path("candidates")
        / "pilot"
        / "metadata.template.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["manual_code_edits"] is False
    assert set(payload["tasks"]) == set(TASK_IDS)


def test_generation_protocol_exists() -> None:
    protocol = (
        Path("docs")
        / "CANDIDATE_GENERATION_PROTOCOL.md"
    )
    assert protocol.is_file()
