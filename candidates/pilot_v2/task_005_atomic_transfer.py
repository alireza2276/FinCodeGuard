def transfer(
    accounts,
    source,
    destination,
    amount,
    authorized,
    simulate_credit_failure=False,
):
    if not authorized:
        raise PermissionError("transfer is not authorized")

    if amount <= 0:
        raise ValueError("amount must be positive")

    if source not in accounts or destination not in accounts:
        raise ValueError("account not found")

    if source == destination:
        raise ValueError("source and destination must be different")

    if accounts[source] < amount:
        raise ValueError("insufficient funds")

    source_balance = accounts[source]
    destination_balance = accounts[destination]

    try:
        accounts[source] = source_balance - amount

        if simulate_credit_failure:
            raise ValueError("simulated credit failure")

        accounts[destination] = destination_balance + amount

    except Exception:
        accounts[source] = source_balance
        accounts[destination] = destination_balance
        raise

    return True
