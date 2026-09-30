from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    payment = candidate.new_payment()
    candidate.transition(
        payment,
        "approved",
        "approver",
    )
    functional_ok = payment["status"] == "approved"

    payment = candidate.new_payment()
    try:
        candidate.transition(
            payment,
            "approved",
            "viewer",
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = True

    payment = candidate.new_payment()
    candidate.transition(
        payment,
        "rejected",
        "approver",
    )
    try:
        candidate.transition(
            payment,
            "settled",
            "approver",
        )
        invariant_ok = False
    except (PermissionError, ValueError):
        invariant_ok = True

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Pending payment can become approved.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Unauthorized transition is rejected.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Rejected payment cannot directly settle.",
        ),
    )
