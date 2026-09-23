# FinCodeGuard Research Methodology

## 1. Research Problem

AI coding agents may generate financial software that satisfies conventional
functional requirements while violating security constraints or
domain-specific financial business invariants.

FinCodeGuard investigates this gap through executable verification.

## 2. Research Questions

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

## 3. Experimental Conditions

### Condition A: Standard Generation

The AI coding agent receives the financial task specification and generates
an implementation without additional security-oriented guidance.

### Condition B: Security-Aware Generation

The AI coding agent receives the same task specification together with
general secure-development instructions.

The prompt must not reveal hidden verification checks.

### Condition C: Verification-Guided Repair

The generated implementation is evaluated by FinCodeGuard.

If verification fails, structured findings are returned to the coding agent.

The agent may generate a repair, after which the complete verification suite
is executed again.

The maximum number of repair iterations must be defined before the main
experiment.

## 4. Verification Dimensions

Candidate implementations may be evaluated across:

- functional correctness
- security requirements
- financial business invariants
- static security analysis
- regression behavior

Executable tests are the primary verification oracle.

Static analysis tools provide supplementary evidence and do not replace
domain-specific executable verification.

## 5. Planned Metrics

Potential metrics include:

- Functional Pass Rate
- Security Pass Rate
- Business-Invariant Pass Rate
- Fully-Correct Rate
- Repair Success Rate
- Regression Rate

The study may also measure conditional failure rates such as:

```text
P(Security Failure | Functional Pass)