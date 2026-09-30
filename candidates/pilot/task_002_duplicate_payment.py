class Payment:
    def __init__(self, payment_id, actor_id, amount, idempotency_key):
        self.payment_id = payment_id
        self.actor_id = actor_id
        self.amount = amount
        self.idempotency_key = idempotency_key


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
        return _payments[key].payment_id

    payment = Payment(
        payment_id=_next_payment_id,
        actor_id=actor_id,
        amount=amount,
        idempotency_key=idempotency_key,
    )

    _payments[key] = payment
    _next_payment_id += 1

    return payment.payment_id