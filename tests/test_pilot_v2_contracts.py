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


def test_contract_version() -> None:
    path = Path("benchmark") / "pilot" / "CONTRACT_VERSION"
    assert path.read_text(encoding="utf-8").strip() == "pilot-v2"


def test_all_v2_prompts_are_frozen() -> None:
    root = Path("prompts") / "pilot_v2"
    for task_id in TASK_IDS:
        content = (root / f"{task_id}.txt").read_text(encoding="utf-8")
        assert "Contract version: pilot-v2" in content
        assert "Do not assume access to benchmark tests" in content


def test_dictionary_contracts_are_explicit() -> None:
    root = Path("prompts") / "pilot_v2"
    task_ids = (
        "task_001_maker_checker",
        "task_002_duplicate_payment",
        "task_003_approved_immutability",
        "task_004_state_transition",
        "task_007_audit_approval",
    )
    for task_id in task_ids:
        content = (root / f"{task_id}.txt").read_text(encoding="utf-8")
        assert "dictionary" in content.lower()


def test_pre_pilot_findings_documented() -> None:
    path = Path("docs") / "PRE_PILOT_FINDINGS.md"
    content = path.read_text(encoding="utf-8").lower()
    assert "benchmark contract ambiguity" in content
    assert "not counted as main pilot model results" in content
