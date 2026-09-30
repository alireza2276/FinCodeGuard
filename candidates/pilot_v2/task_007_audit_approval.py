def new_payment():
    return {
        "status": "pending",
    }


def approve(payment, actor_id, role, audit_log):
    if not isinstance(payment, dict):
        raise ValueError("payment must be a dictionary")

    if payment.get("status") != "pending":
        raise ValueError("payment is not pending")

    if role != "checker":
        raise PermissionError("only a checker may approve a payment")

    payment["status"] = "approved"

    audit_log.append({
        "action": "payment_approved",
        "actor_id": actor_id,
    })

    return payment
