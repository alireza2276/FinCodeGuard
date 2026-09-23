# FinCodeGuard Benchmark

## 1. Purpose

The FinCodeGuard benchmark evaluates AI-generated implementations of
financial software requirements using executable verification.

## 2. Development Strategy

A small pilot benchmark should be developed first to validate task structure,
specifications, verification oracles, experimental workflow, and failure
reporting. After validation, the benchmark may be expanded and frozen before
the main experiment.

## 3. Planned Task Structure

```text
task_xxx/
|-- specification.yaml
|-- metadata.yaml
|-- starter_repo/
`-- tests/
    |-- test_functional.py
    |-- test_security.py
    `-- test_invariants.py
```

## 4. Requirement Types

A task specification may contain:
- functional requirements
- security requirements
- business invariants
- preconditions
- postconditions
- allowed behavior
- forbidden behavior

## 5. Candidate Invariant Categories

Initial categories include separation of duties, authorization and ownership,
state-transition integrity, transaction immutability, idempotency and
duplicate prevention, atomicity, concurrency integrity, auditability,
sensitive-data handling, and amount/currency integrity.

## 6. Benchmark Integrity

Tasks should use synthetic data, avoid real customer or banking credentials,
be deterministic where practical, and distinguish functional requirements
from security requirements and domain-specific business invariants.

## 7. Interpretation

Passing a benchmark task does not demonstrate production-level financial
software security. A PASS means only that the candidate implementation
satisfied the verification oracles defined for that task.
