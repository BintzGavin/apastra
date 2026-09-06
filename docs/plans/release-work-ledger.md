# Release work ownership

Target: `gavin/fix-evaluation-trust`, isolated checkout `/private/tmp/apastra-trust.hQdcnc/checkout`.
Integrator: this coordinating Apastra task. No worker may commit, push, publish, or change another owner's files.

| Ticket | State | Owner | Scope |
| --- | --- | --- | --- |
| TRUST | in_scope | integrator | Runtime repairs and regression tests, installed-package checks, migration documentation |
| CI-FALSE-PASS | deferred | integrator | Separate narrow repair of the existing report gate. Keep existing check names and workflow structure. Acceptance cases live in the P0 plan. |
| CI-REDESIGN | dropped | none | New jobs, check renaming, broad workflow replacement, mandatory dogfooding, and release automation redesign are outside this change. |
| PACKAGE | already_done | integrator (handoff received) | Missing manifests repaired in npm and clone layouts; 6 tests passed in worker verification. Integrator owns all files again. |
| VALIDATOR | already_done | integrator | Offline shared AJV lookup; preserve handoff repair |
| RESEARCH | excluded | user | Untracked main-checkout research; not part of release |
| PLATFORMS | excluded | none | Hosted execution, cryptographic signing, alert delivery, automated rollback, optimizer implementation |
| QUALITY | ambiguous | integrator | “Dax/OpenCode level” is a quality bar, not permission to copy unrelated architecture |

PACKAGE stopping rule: one bounded repair and verification pass; report changes, test commands, blockers, and exact package/runtime gaps. Main agent independently reruns integration gates. No other task writes to the main checkout. Corrections must be recorded here and acknowledged before affected work resumes.

Correction, September 5, 2026: `setup.py` was an incorrect filename; PACKAGE owns the actual `setup` shell script. Scope otherwise unchanged.

Scope approved September 6, 2026: retain the implemented runtime and packaging
repairs. Verify them locally and keep the CI false-pass repair separate. The
rejected broad workflow patch was never applied. Version 2.0.0 is selected for
the incompatible protocol changes. Publication remains uncompleted because npm
authentication returned HTTP 401 during the release checks.
