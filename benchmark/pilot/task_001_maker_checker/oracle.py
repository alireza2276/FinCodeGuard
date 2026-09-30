from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    payment = candidate.create_payment("maker-1", 100)
    functional_ok = payment["status"] == "pending"

    try:
        candidate.approve_payment(
            payment,
            "user-1",
            "maker",
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = True

    payment = candidate.create_payment("maker-1", 100)
    try:
        candidate.approve_payment(
            payment,
            "maker-1",
            "checker",
        )
        invariant_ok = False
    except (PermissionError, ValueError):
        invariant_ok = True

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Maker can create a pending payment.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Non-checker approval is rejected.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Maker cannot approve own payment.",
        ),
    )
