# FinCodeGuard Quality Gate

The Stage 8C quality gate defines the minimum engineering checks required
before the pilot research release.

## Required checks

The gate runs:

1. Ruff static style and lint checks.
2. The complete pytest suite.
3. Branch-aware coverage measurement for the `fincodeguard` package.
4. XML coverage output for CI or later reporting.
5. A minimum total coverage threshold of 70%.

Run the complete gate from the repository root:

```powershell
python scripts/quality_gate.py
```

The command exits with a non-zero status if Ruff, pytest, or the coverage
threshold fails.

## Individual commands

Lint only:

```powershell
ruff check .
```

Tests with coverage:

```powershell
pytest --cov=fincodeguard --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml --cov-fail-under=70
```

Docker verification remains a separate release check:

```powershell
docker compose build
docker compose run --rm fincodeguard
```

## Coverage policy

The 70% threshold is a pilot-release floor, not a claim of production
readiness. Coverage is only one signal. Executable financial invariants,
security checks, benchmark validity, and isolation of untrusted generated
code remain separate concerns.

The threshold should only be raised after missing lines have been reviewed.
Tests should not be added merely to inflate the percentage.
