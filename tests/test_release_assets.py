from pathlib import Path


def test_release_documentation_exists() -> None:
    assert Path("RELEASE_CHECKLIST.md").is_file()
    assert (
        Path("docs")
        / "PILOT_PROTOCOL.md"
    ).is_file()


def test_pilot_script_exists() -> None:
    script = Path("scripts") / "run_pilot.py"
    assert script.is_file()

    content = script.read_text(encoding="utf-8")
    assert "run_pilot_suite" in content
    assert "pilot_summary.json" in content
