# Pilot v2 Oracle Contracts

Pilot v2 freezes the observable interfaces used by the executable oracles.

Tasks 001, 002, 003, 004, and 007 explicitly require dictionary-based observable
payment data because the corresponding oracles use dictionary access. Task 005
uses a mutable balance dictionary. Task 006 exposes Account.balance. Task 008
uses a mutable log list.

The generation-facing normative contracts are the frozen files in
`prompts/pilot_v2/`. Oracle implementation source remains hidden from candidate
generation.
