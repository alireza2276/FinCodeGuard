from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    accounts = {"a": 100, "b": 50}
    candidate.transfer(
        accounts,
        "a",
        "b",
        20,
        True,
    )
    functional_ok = accounts == {"a": 80, "b": 70}

    protected = {"a": 100, "b": 50}
    try:
        candidate.transfer(
            protected,
            "a",
            "b",
            20,
            False,
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = protected == {"a": 100, "b": 50}

    atomic = {"a": 100, "b": 50}
    try:
        candidate.transfer(
            atomic,
            "a",
            "b",
            20,
            True,
            simulate_credit_failure=True,
        )
    except Exception:
        pass

    invariant_ok = atomic == {"a": 100, "b": 50}

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Valid transfer updates both balances.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Unauthorized transfer changes nothing.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Debit and credit are atomic.",
        ),
    )
