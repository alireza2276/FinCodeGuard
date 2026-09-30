class Payment:
    def __init__(self):
        self.status = "pending"


def new_payment():
    return Payment()


def transition(payment, target_status, actor_role):
    if not isinstance(payment, Payment):
        raise ValueError("invalid payment")

    if actor_role != "approver":
        raise PermissionError("only authorized approvers may perform transitions")

    valid_transitions = {
        "pending": {"approved", "rejected"},
        "approved": {"settled", "rejected"},
        "rejected": set(),
        "settled": set(),
    }

    if payment.status not in valid_transitions:
        raise ValueError("invalid current status")

    if target_status not in valid_transitions:
        raise ValueError("invalid target status")

    if target_status not in valid_transitions[payment.status]:
        raise ValueError(
            f"invalid transition from {payment.status} to {target_status}"
        )

    payment.status = target_status
    return payment