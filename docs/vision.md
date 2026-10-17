# Apastra product direction

Apastra should earn its place as a portable evidence and release-decision layer for teams that already run evals. The first user is a small engineering team that needs a reviewer or CI job to independently check results produced elsewhere.

The product question is concrete: can a team move an evaluation run between checkouts, prove which inputs and declared adapter files it belongs to, inspect losing candidates, and block a release when any required model regresses—without rebuilding its execution stack?

## Why another tool might be needed

Existing eval tools already provide datasets, assertions, execution, comparisons and CI. These are prerequisites, not a differentiation claim. Promptfoo itself supports [configuration and exported results](https://www.promptfoo.dev/docs/configuration/outputs/). Apastra should integrate with those tools and compete with the team's evidence-verification glue.

The proposed advantage is one independently inspectable contract for retained runs, per-model decisions, portable baselines and revision-bound admission across harnesses. This remains a product hypothesis. A collection of schemas, a large local research corpus, or passing software tests does not establish customer demand.

Use an existing runner directly when its result storage and gate semantics already meet the team's needs. Add Apastra when the independent review boundary removes more maintenance work than the adapter and evidence format introduce.

## What this candidate establishes

- Complete failing measurements remain available in comparisons.
- Each requested model must satisfy thresholds and blocking regression rules.
- CI rejects missing configuration, missing evidence, stale revisions and mismatched input snapshots.
- Adapter identity explicitly distinguishes configuration-only records from pinned declared implementation files.
- Baselines reference retained runs relative to the baseline record, so a workspace and its evidence can move together.
- Installation preserves source control and user edits; the Python runtime can be installed without Node.
- A maintained Promptfoo quick-eval bridge supplies a narrow integration seam; its documented supported modes and tests define its limits.

These changes are version 3 contract work. Historical runs stay historical; rerun them to obtain current decisions. They are not proof of live-provider reliability, authenticated provenance or statistical significance.

## Deliberate limits

No hosted runner, provider abstraction platform, public registry, automatic optimization, scheduled canary service, delivery system or rollback engine is part of the supported core. Existing design schemas remain available for history and discussion; they do not expand the shipped promise. Provider request logging and agent hooks are optional debugging aids, not the reason to adopt the verifier.

Do not expand the schema surface until an implemented workflow needs it. Do not add a new execution engine where an existing harness can supply outputs. Do not describe content hashes as authenticity or guaranteed reproducibility.

## Next product proof

Use one real team's existing Promptfoo evaluation and one real release decision. Compare direct Promptfoo plus their current scripts against the Apastra bridge. Measure setup effort, extra files to maintain, time to explain a rejected run, and whether a second checkout can independently reproduce the decision. Keep the integration only if the evidence boundary removes a concrete recurring burden.

A failure to beat that baseline is a reason to simplify or stop, not to add more product domains.
