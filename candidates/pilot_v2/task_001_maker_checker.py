def create_payment(maker_id, amount):
    if maker_id is None:
        raise ValueError("maker_id is required")

    if amount <= 0:
        raise ValueError("amount must be positive")

    return {
        "maker_id": maker_id,
        "amount": amount,
        "status": "pending",
        "approved_by": None,
    }


def approve_payment(payment, actor_id, role):
    if not isinstance(payment, dict):
        raise ValueError("payment must be a dictionary")

    required_fields = {"maker_id", "amount", "status", "approved_by"}

    if not required_fields.issubset(payment):
        raise ValueError("invalid payment")

    if payment["status"] != "pending":
        raise ValueError("payment is not pending")

    if role != "checker":
        raise PermissionError("only a checker may approve a payment")

    if actor_id == payment["maker_id"]:
        raise PermissionError("maker cannot approve their own payment")

    payment["status"] = "approved"
    payment["approved_by"] = actor_id

    return payment
