from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    logs = []
    candidate.process_payment(
        100,
        "u1",
        "SECRET-TOKEN",
        logs,
    )
    text = " ".join(map(str, logs))

    functional_ok = bool(logs)
    security_ok = "SECRET-TOKEN" not in text
    invariant_ok = (
        "u1" in text
        and "100" in text
    )

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Workflow emits operational logs.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Authentication secret is absent from logs.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Required audit context remains in logs.",
        ),
    )
