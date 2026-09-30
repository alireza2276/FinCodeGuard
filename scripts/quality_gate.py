from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QualityCheck:
    name: str
    command: tuple[str, ...]


CHECKS = (
    QualityCheck(
        name="Ruff",
        command=("ruff", "check", "."),
    ),
    QualityCheck(
        name="Tests and coverage",
        command=(
            "pytest",
            "--cov=fincodeguard",
            "--cov-config=.coveragerc",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=70",
        ),
    ),
)


def run_check(check: QualityCheck) -> int:
    print(f"\n==> {check.name}")
    print("$ " + " ".join(check.command))
    completed = subprocess.run(
        check.command,
        check=False,
    )
    return completed.returncode


def main() -> int:
    for check in CHECKS:
        exit_code = run_check(check)
        if exit_code != 0:
            print(
                f"\nQUALITY GATE FAILED: {check.name}",
                file=sys.stderr,
            )
            return exit_code

    print("\nQUALITY GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
