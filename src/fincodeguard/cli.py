from __future__ import annotations

import argparse
from pathlib import Path

from fincodeguard.experiments.end_to_end import run_pilot_candidate
from fincodeguard.reporting.json_reporter import write_json_report
from fincodeguard.reporting.text_reporter import render_text_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fincodeguard",
        description="Verify a candidate against a FinCodeGuard pilot task.",
    )
    parser.add_argument(
        "task_directory",
        type=Path,
        help="Path to a pilot benchmark task directory.",
    )
    parser.add_argument(
        "candidate",
        type=Path,
        help="Path to the candidate Python implementation.",
    )
    parser.add_argument(
        "--json-report",
        type=Path,
        default=None,
        help="Optional output path for a JSON verification report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    result = run_pilot_candidate(
        args.task_directory,
        args.candidate,
    )
    print(render_text_report(result.report))

    if args.json_report is not None:
        write_json_report(
            result.report,
            args.json_report,
        )

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
