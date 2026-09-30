def new_payment():
    return {
        "status": "pending",
    }


def transition(payment, target_status, actor_role):
    if not isinstance(payment, dict):
        raise ValueError("payment must be a dictionary")

    if "status" not in payment:
        raise ValueError("invalid payment")

    if actor_role != "approver":
        raise PermissionError("only an approver may transition a payment")

    valid_transitions = {
        "pending": {"approved", "rejected"},
        "approved": set(),
        "rejected": set(),
        "settled": set(),
    }

    current_status = payment["status"]

    if current_status not in valid_transitions:
        raise ValueError("invalid current status")

    if target_status not in valid_transitions:
        raise ValueError("invalid target status")

    if target_status not in valid_transitions[current_status]:
        raise ValueError(
            f"invalid transition from {current_status} to {target_status}"
        )

    payment["status"] = target_status

    return payment
