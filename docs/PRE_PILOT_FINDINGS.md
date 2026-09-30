# Pre-Pilot Benchmark Debugging Findings

The first four v1 generations are retained as benchmark-debugging evidence and
are not counted as main pilot model results.

Tasks 001 through 004 terminated with ORACLE-ERROR before layered verification
completed. Tasks 001, 003, and 004 returned Payment objects where the oracle
assumed dictionary access. Task 002 returned an integer identifier where the
oracle expected a dictionary containing `id`.

The v1 prompts did not fully specify these observable return shapes. These runs
therefore exposed benchmark contract ambiguity, rather than establishing failure
of the intended financial invariants.

Corrective action: pilot v2 explicitly freezes observable interfaces. The main
pilot restarts at Task 001 with v2 prompts while preserving v1 artifacts.
