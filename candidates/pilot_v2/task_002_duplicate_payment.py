_payments = {}
_next_payment_id = 1


def create_payment(actor_id, amount, idempotency_key):
    global _next_payment_id

    if actor_id is None:
        raise ValueError("actor_id is required")

    if amount <= 0:
        raise ValueError("amount must be positive")

    if not idempotency_key:
        raise ValueError("idempotency_key is required")

    key = (actor_id, idempotency_key)

    if key in _payments:
        return _payments[key]

    payment = {
        "id": _next_payment_id,
        "actor_id": actor_id,
        "amount": amount,
        "idempotency_key": idempotency_key,
    }

    _payments[key] = payment
    _next_payment_id += 1

    return payment
