# Candidate Generation Protocol

## Purpose

This protocol separates candidate generation from executable evaluation so the pilot does not
accidentally teach the candidate generator how the oracle is implemented.

## Before generation

1. Freeze the prompt files under `prompts/pilot/`.
2. Record the FinCodeGuard Git commit.
3. Copy `candidates/pilot/metadata.template.json` to a run-specific metadata file.
4. Fill in provider, model, date, condition, and available generation settings.

## Generation

Generate exactly one candidate per frozen task prompt for the first baseline run.

Store raw Python outputs as:

- `candidates/pilot/task_001_maker_checker.py`
- `candidates/pilot/task_002_duplicate_payment.py`
- `candidates/pilot/task_003_approved_immutability.py`
- `candidates/pilot/task_004_state_transition.py`
- `candidates/pilot/task_005_atomic_transfer.py`
- `candidates/pilot/task_006_concurrent_withdrawal.py`
- `candidates/pilot/task_007_audit_approval.py`
- `candidates/pilot/task_008_sensitive_logging.py`

Do not repair or manually correct a baseline candidate before its first verification.

## Evaluation

After all eight raw candidates are preserved, run:

```powershell
python scripts/run_pilot.py candidates/pilot
```

Preserve `results/pilot_summary.json` together with the candidate set and metadata.

## Repair experiments

Repair is a separate condition. Never overwrite the baseline candidate. Save repaired candidates
under a separate run directory or with a clearly versioned name and preserve the feedback supplied
to the model.

## Interpretation

The first eight-candidate run is a feasibility pilot, not a statistically powered benchmark.
Do not claim model superiority, statistical significance, or production banking readiness from it.
