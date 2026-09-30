from concurrent.futures import ThreadPoolExecutor

from fincodeguard.verification.oracle import OracleCheck
from fincodeguard.verification.result import VerificationCategory


def evaluate(candidate):
    account = candidate.Account(100)
    result = candidate.withdraw(
        account,
        20,
        True,
    )
    functional_ok = result is True and account.balance == 80

    protected = candidate.Account(100)
    try:
        candidate.withdraw(
            protected,
            20,
            False,
        )
        security_ok = False
    except (PermissionError, ValueError):
        security_ok = protected.balance == 100

    concurrent_account = candidate.Account(100)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                lambda _: candidate.withdraw(
                    concurrent_account,
                    80,
                    True,
                ),
                range(2),
            )
        )

    successful = sum(bool(value) for value in results)
    invariant_ok = (
        concurrent_account.balance >= 0
        and successful <= 1
    )

    return (
        OracleCheck(
            "FUNC-001",
            VerificationCategory.FUNCTIONAL,
            functional_ok,
            "Valid withdrawal reduces the balance.",
        ),
        OracleCheck(
            "SEC-001",
            VerificationCategory.SECURITY,
            security_ok,
            "Unauthorized withdrawal is rejected.",
        ),
        OracleCheck(
            "INV-001",
            VerificationCategory.BUSINESS_INVARIANT,
            invariant_ok,
            "Concurrent withdrawals preserve the balance constraint.",
        ),
    )
