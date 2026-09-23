# FinCodeGuard Threat Model

## 1. Objective

This document defines initial application-level failure classes that
FinCodeGuard may evaluate. It does not model every threat relevant to
production financial systems.

## 2. Protected Assets

Depending on the task, protected assets may include financial transaction
state, payment authorization state, account ownership boundaries, workflow
integrity, audit records, and sensitive financial information.

## 3. Threat Actors

### Unauthorized Actor
A user or request without sufficient authorization attempts a protected
financial operation.

### Authorized but Constrained Actor
A legitimate user attempts an operation prohibited by a financial business
rule, such as a payment creator approving their own payment.

### Replay or Duplicate Actor
A valid financial operation is submitted repeatedly in an attempt to produce
duplicate financial effects.

### Concurrent Actor
Multiple valid-looking operations execute concurrently and attempt to bypass
state, authorization, or transaction-integrity constraints.

## 4. Example Properties

Potential properties include role-based approval, maker-checker separation,
immutability after approval, duplicate prevention, atomic state changes,
valid workflow transitions, sensitive-data protection, and audit creation.

## 5. Out of Scope for Version 1

Unless explicitly required by a benchmark task, Version 1 does not attempt
to evaluate operating-system compromise, database-server compromise,
cloud-infrastructure compromise, cryptographic algorithm design,
side-channel attacks, direct malicious database administration,
comprehensive supply-chain attacks, or production banking certification.

## 6. Interpretation of PASS

A FinCodeGuard PASS does not prove that software is secure or safe for
production. It means only that the implementation satisfied the verification
oracles defined for the corresponding benchmark task.
