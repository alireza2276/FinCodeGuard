import threading


class Account:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("balance cannot be negative")

        self.balance = balance
        self._lock = threading.Lock()


def withdraw(account, amount, authorized):
    if not isinstance(account, Account):
        raise ValueError("invalid account")

    if not authorized:
        raise PermissionError("withdrawal is not authorized")

    if amount <= 0:
        raise ValueError("amount must be positive")

    with account._lock:
        if account.balance < amount:
            return False

        account.balance -= amount
        return True
