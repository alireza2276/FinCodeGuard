from __future__ import annotations

import argparse
from pathlib import Path

from fincodeguard.experiments.pilot import (
    run_pilot_suite,
    write_pilot_summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the FinCodeGuard pilot benchmark.",
    )
    parser.add_argument(
        "candidates",
        type=Path,
        help="Directory containing one candidate Python file per pilot task.",
    )
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=Path("benchmark") / "pilot",
        help="Pilot benchmark directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results") / "pilot_summary.json",
        help="Output path for the pilot summary.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    summary = run_pilot_suite(
        args.benchmark,
        args.candidates,
    )
    output = write_pilot_summary(
        summary,
        args.output,
    )

    print(f"Pilot tasks: {summary.total_tasks}")
    print(f"Passed: {summary.passed_tasks}")
    print(f"Failed: {summary.failed_tasks}")
    print(f"Pass rate: {summary.pass_rate:.1%}")
    print(f"Summary: {output}")

    return 0 if summary.failed_tasks == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
