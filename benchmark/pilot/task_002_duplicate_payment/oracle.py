from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    first = candidate.create_payment("u1", 100, "k1")
    duplicate = candidate.create_payment("u1", 100, "k1")
    other_actor = candidate.create_payment("u2", 100, "k1")

    functional_ok = first is not None
    security_ok = other_actor["id"] != first["id"]
    invariant_ok = duplicate["id"] == first["id"]

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Valid request creates a payment.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Idempotency key is scoped to the actor.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Replay creates no second financial effect.",
        ),
    )
