# FinCodeGuard

**A Verification Framework for AI-Generated Financial Software**

FinCodeGuard is a research-oriented framework for evaluating whether
AI-generated financial software satisfies not only functional requirements,
but also security requirements and domain-specific financial business
invariants.

## Research Motivation

AI coding agents can generate implementations that appear functionally
correct while still violating security constraints or financial business
rules.

FinCodeGuard investigates this gap using executable verification of
functional requirements, security requirements, and domain-specific
financial invariants.

## Core Research Question

> Can functionally correct AI-generated financial software still violate
> security and domain-specific business invariants, and can an automated
> verification loop detect and reduce these failures before integration?

## Research Questions

### RQ1

Among AI-generated financial implementations that satisfy their functional
requirements, how frequently do they violate security requirements or
domain-specific financial business invariants?

### RQ2

Which categories of financial business invariants and security requirements
are most difficult for AI coding agents to satisfy reliably?

### RQ3

Can verification-guided feedback reduce security and financial
business-invariant violations without introducing functional regressions?

## Research Focus

Initial verification targets include:

- separation of duties
- authorization and ownership
- transaction integrity
- transaction immutability
- state-transition integrity
- idempotency and duplicate prevention
- atomicity
- concurrency integrity
- auditability
- sensitive-data handling

## Planned Experimental Conditions

FinCodeGuard is designed to support comparison between:

1. Standard AI generation
2. Security-aware AI generation
3. FinCodeGuard verification-guided repair

## Verification Pipeline

```text
Financial Task Specification
        |
        v
AI Coding Agent
        |
        v
Generated Code / Patch
        |
        v
FinCodeGuard
        |
        +-- Functional Verification
        +-- Security Verification
        +-- Financial Business-Invariant Verification
        +-- Static Analysis
        +-- Regression Verification
        |
        v
PASS / REJECT
        |
        v
Structured Feedback
        |
        v
AI Repair
        |
        v
Re-verification