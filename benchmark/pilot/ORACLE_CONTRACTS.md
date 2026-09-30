# Pilot Oracle Candidate Contracts

Stage 8A makes the eight pilot specifications executable.

1. Maker-checker:
   `create_payment(maker_id, amount)` and
   `approve_payment(payment, actor_id, role)`.
2. Duplicate payment:
   `create_payment(actor_id, amount, idempotency_key)`.
3. Approved immutability:
   `create_payment(amount, beneficiary)`,
   `edit_payment(...)`, and `approve_payment(payment)`.
4. State transition:
   `new_payment()` and
   `transition(payment, target_status, actor_role)`.
5. Atomic transfer:
   `transfer(accounts, source, destination, amount, authorized,
   simulate_credit_failure=False)`.
6. Concurrent withdrawal:
   `Account(balance)` and
   `withdraw(account, amount, authorized) -> bool`.
7. Audit approval:
   `new_payment()` and
   `approve(payment, actor_id, role, audit_log)`.
8. Sensitive logging:
   `process_payment(amount, actor_id, auth_token, logs)`.

These are pilot contracts, not production banking APIs.
Freeze the contracts before the main experiment.
