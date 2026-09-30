from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from fincodeguard.verification.result import (
    VerificationCategory,
    VerificationFinding,
    VerificationReport,
    VerificationStatus,
)


@dataclass(frozen=True, slots=True)
class OracleCheck:
    check_id: str
    category: VerificationCategory
    passed: bool
    message: str


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_python_oracle(
    task_id: str,
    oracle_path: str | Path,
    candidate_path: str | Path,
) -> VerificationReport:
    oracle_file = Path(oracle_path)
    candidate_file = Path(candidate_path)

    if not oracle_file.is_file():
        raise FileNotFoundError(
            f"Oracle file does not exist: {oracle_file}"
        )
    if not candidate_file.is_file():
        raise FileNotFoundError(
            f"Candidate file does not exist: {candidate_file}"
        )

    try:
        oracle_module = _load_module(
            oracle_file,
            f"oracle_{task_id}",
        )
        candidate_module = _load_module(
            candidate_file,
            f"candidate_{task_id}",
        )
        checks = oracle_module.evaluate(candidate_module)
    except Exception as exc:
        finding = VerificationFinding(
            "ORACLE-ERROR",
            VerificationCategory.FUNCTIONAL,
            VerificationStatus.ERROR,
            (
                "Oracle execution failed: "
                f"{type(exc).__name__}: {exc}"
            ),
        )
        return VerificationReport(task_id, (finding,))

    findings = tuple(
        VerificationFinding(
            check.check_id,
            check.category,
            (
                VerificationStatus.PASS
                if check.passed
                else VerificationStatus.FAIL
            ),
            check.message,
        )
        for check in checks
    )
    return VerificationReport(task_id, findings)
