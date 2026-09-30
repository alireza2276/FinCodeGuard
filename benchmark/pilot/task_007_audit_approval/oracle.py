from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    audit_log = []
    payment = candidate.new_payment()
    candidate.approve(
        payment,
        "checker-1",
        "checker",
        audit_log,
    )
    functional_ok = payment["status"] == "approved"

    other_payment = candidate.new_payment()
    try:
        candidate.approve(
            other_payment,
            "u1",
            "viewer",
            audit_log,
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = True

    matching_events = [
        event
        for event in audit_log
        if (
            event.get("action") == "payment_approved"
            and event.get("actor_id") == "checker-1"
        )
    ]
    invariant_ok = len(matching_events) == 1

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Authorized checker can approve.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Unauthorized approval is rejected.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Approval creates one attributable audit event.",
        ),
    )
