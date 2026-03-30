# Quick Eval Policy

## 1. Scope and Purpose
The "Quick eval mode" is intended exclusively for rapid iteration, local smoke testing, and early-stage prompt development. It allows authors to combine prompt templates, datasets, and inline assertions into a single .yaml file for immediate feedback.

Quick evals must not be used as formal release candidates, nor should they be the primary gating mechanism for promoting prompt packages to production channels.

## 2. Limitations and Graduation Rules
To prevent quick eval files from becoming unmaintainable monoliths and to ensure adequate test coverage, the following limits are enforced:

- Maximum Test Cases: A quick eval file may contain no more than 20 dataset cases.
- Maximum Assertions: A quick eval file may contain no more than 20 inline assertions total across all cases.

Once a quick eval file exceeds either of these limits, it must be refactored (graduated) into the full protocol structure:
- A standalone prompt-spec file.
- A standalone dataset file.
- A standalone evaluator file.
- A standalone suite file referencing the above.

## 3. Enforcement
- Automated validation workflows will enforce the maximum case and assertion limits.
- Pull Requests introducing or modifying quick eval files that exceed these limits will fail validation and be blocked from merging.
- Human reviewers should guide authors to refactor complex quick evals into formal suites.
