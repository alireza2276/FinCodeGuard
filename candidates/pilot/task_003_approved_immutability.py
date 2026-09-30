class Payment:
    def __init__(self, amount, beneficiary):
        if amount <= 0:
            raise ValueError("amount must be positive")

        if not beneficiary:
            raise ValueError("beneficiary is required")

        self.amount = amount
        self.beneficiary = beneficiary
        self.status = "pending"


def create_payment(amount, beneficiary):
    return Payment(amount, beneficiary)


def edit_payment(payment, amount=..., actor_role=...):
    if not isinstance(payment, Payment):
        raise ValueError("invalid payment")

    if payment.status != "pending":
        raise PermissionError("approved payment cannot be edited")

    if actor_role != "editor":
        raise PermissionError("only authorized editors may edit payments")

    if amount is ...:
        raise ValueError("amount is required")

    if amount <= 0:
        raise ValueError("amount must be positive")

    payment.amount = amount
    return payment


def approve_payment(payment):
    if not isinstance(payment, Payment):
        raise ValueError("invalid payment")

    if payment.status != "pending":
        raise ValueError("payment is not pending")

    payment.status = "approved"
    return payment