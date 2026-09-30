# FinCodeGuard v0.1.0 Release Checklist

This checklist defines the evidence required before creating the first
public pilot release.

## Engineering gate

- [ ] `ruff check .` passes.
- [ ] `pytest` passes.
- [ ] `python scripts/quality_gate.py` passes.
- [ ] Docker image builds successfully.
- [ ] The complete test suite passes inside Docker.
- [ ] GitHub Actions is green on the release commit.

## Benchmark gate

- [ ] All eight pilot task specifications are present.
- [ ] All eight executable pilot oracles are present.
- [ ] Candidate contracts are frozen for the pilot experiment.
- [ ] Pilot candidates are versioned or otherwise reproducibly identified.
- [ ] Raw pilot results are preserved.
- [ ] No synthetic test result is presented as an empirical research result.

## Documentation gate

- [ ] README describes the implemented architecture.
- [ ] README clearly separates implemented features from planned work.
- [ ] Pilot methodology is documented.
- [ ] Limitations are documented.
- [ ] Security limitations of in-process candidate execution are disclosed.
- [ ] Reported metrics are derived from preserved experiment outputs.

## Release gate

- [ ] Working tree is clean.
- [ ] Version is tagged as `v0.1.0`.
- [ ] Release notes describe the pilot scope and limitations.
- [ ] The GitHub release does not make unsupported novelty claims.

Only create `v0.1.0` after every applicable item above has been verified.
