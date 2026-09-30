# FinCodeGuard Pilot Protocol

## Objective

The pilot evaluates whether FinCodeGuard can distinguish candidate
implementations that satisfy functional, security, and financial business
invariant checks across the eight pilot tasks.

The pilot is an engineering and feasibility evaluation. It is not, by
itself, evidence that FinCodeGuard is superior to existing systems.

## Benchmark

The pilot benchmark contains eight financial-software tasks:

1. Maker-checker separation.
2. Duplicate-payment prevention.
3. Approved-payment immutability.
4. State-transition integrity.
5. Atomic transfer.
6. Concurrent withdrawal.
7. Approval auditability.
8. Sensitive-data logging.

Each task has a specification and an executable oracle. Candidate APIs must
follow `benchmark/pilot/ORACLE_CONTRACTS.md`.

## Candidate identification

Candidate implementations used in an experiment should be preserved in a
versioned directory. The model name, model version when available, prompt
condition, date, and relevant generation settings should be recorded outside
the candidate source or in experiment metadata.

Do not overwrite candidates after recording results.

## Execution

Run the engineering quality gate first:

```powershell
python scripts/quality_gate.py
```

Then run the pilot:

```powershell
python scripts/run_pilot.py candidates/pilot
```

The default machine-readable output is:

```text
results/pilot_summary.json
```

Preserve this output with the corresponding candidate set and Git commit.

## Interpretation

A task passes only when its executable verification report passes. A pilot
pass rate is the fraction of pilot tasks whose complete reports pass.

A pilot pass rate must not be generalized to real banking systems. The eight
tasks are a deliberately small feasibility benchmark.

## Reproducibility

For a result intended for publication or supervisor discussion, preserve:

- FinCodeGuard Git commit.
- Candidate source files.
- Candidate-generation metadata.
- Raw verification outputs.
- Pilot summary.
- Python and dependency versions.
- Execution environment.

## Security limitation

Stage 8A/8D loads candidate Python code in-process. Therefore arbitrary
untrusted generated code must not be executed outside a controlled local
pilot environment. Stronger sandboxing is future work before broader use.

## Research claims

Do not claim novelty, superiority, statistical significance, or production
banking readiness from the pilot alone. Those claims require appropriate
literature review, baselines, experimental design, and evidence.
