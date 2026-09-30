from configparser import ConfigParser
from pathlib import Path


def test_coverage_configuration_targets_package() -> None:
    config_path = Path(".coveragerc")
    assert config_path.is_file()

    config = ConfigParser()
    config.read(config_path, encoding="utf-8")

    assert config.getboolean("run", "branch") is True
    assert config.get("run", "source") == "fincodeguard"
    assert config.get("xml", "output") == "coverage.xml"


def test_quality_gate_script_exists() -> None:
    script = Path("scripts") / "quality_gate.py"
    assert script.is_file()

    content = script.read_text(encoding="utf-8")

    assert "ruff" in content
    assert "pytest" in content
    assert "--cov=fincodeguard" in content
    assert "--cov-fail-under=70" in content
