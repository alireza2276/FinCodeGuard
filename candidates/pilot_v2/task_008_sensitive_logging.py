def process_payment(amount, actor_id, auth_token, logs):
    if amount <= 0:
        raise ValueError("amount must be positive")

    if actor_id is None:
        raise ValueError("actor_id is required")

    if not auth_token:
        raise PermissionError("auth_token is required")

    if not isinstance(logs, list):
        raise ValueError("logs must be a list")

    logs.append({
        "action": "payment_processed",
        "actor_id": actor_id,
        "amount": amount,
    })

    return True
