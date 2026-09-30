def create_payment(amount, beneficiary):
    if amount <= 0:
        raise ValueError("amount must be positive")

    if not beneficiary:
        raise ValueError("beneficiary is required")

    return {
        "amount": amount,
        "beneficiary": beneficiary,
        "status": "pending",
    }


def edit_payment(payment, amount=..., actor_role=...):
    if not isinstance(payment, dict):
        raise ValueError("payment must be a dictionary")

    required_fields = {"amount", "beneficiary", "status"}

    if not required_fields.issubset(payment):
        raise ValueError("invalid payment")

    if payment["status"] != "pending":
        raise PermissionError("approved payment cannot be edited")

    if actor_role != "editor":
        raise PermissionError("only an editor may edit a payment")

    if amount is ...:
        raise ValueError("amount is required")

    if amount <= 0:
        raise ValueError("amount must be positive")

    payment["amount"] = amount

    return payment


def approve_payment(payment):
    if not isinstance(payment, dict):
        raise ValueError("payment must be a dictionary")

    required_fields = {"amount", "beneficiary", "status"}

    if not required_fields.issubset(payment):
        raise ValueError("invalid payment")

    if payment["status"] != "pending":
        raise ValueError("payment is not pending")

    payment["status"] = "approved"

    return payment
