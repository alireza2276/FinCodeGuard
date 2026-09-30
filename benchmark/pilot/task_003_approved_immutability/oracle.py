from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    payment = candidate.create_payment(100, "beneficiary-a")
    candidate.edit_payment(
        payment,
        amount=120,
        actor_role="editor",
    )
    functional_ok = payment["amount"] == 120

    try:
        candidate.edit_payment(
            payment,
            amount=130,
            actor_role="viewer",
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = True

    candidate.approve_payment(payment)
    try:
        candidate.edit_payment(
            payment,
            amount=999,
            actor_role="editor",
        )
        invariant_ok = False
    except (PermissionError, ValueError):
        invariant_ok = True

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Pending payment is editable.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Unauthorized edit is rejected.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Approved fields are immutable.",
        ),
    )
