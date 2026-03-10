# apastra
Prompt versioning, evals, benchmarks, and delivery

## Executive summary

This document proposes a state-of-the-art PromptOps architecture that makes prompts behave like disciplined software assets while keeping day-to-day developer workflow low friction. The system is repo-native and uses entity["company","GitHub","code hosting platform"] as the canonical control plane for versioning, diffs, review, rollback, and auditability via pull requests, required status checks, branch protection, tags, releases, and audit logs. citeturn0search0turn0search1turn1search1turn0search6

It is Black Hole Architecture aligned: file-based durable state is the source of truth; computation is stateless and replaceable; derived results are append-friendly and immutable where possible; end states and transitions are explicit; humans approve at clear checkpoints; autonomous agents can safely operate by generating files and PRs rather than mutating hidden databases. Execution is bring-your-own via a minimal harness contract (“run request in, run artifact out”), so the system does not lock teams into any evaluator framework, agent SDK, provider SDK, runtime, or hosted platform.

Consumption is Git-first. Local overrides and git-ref pins (commit SHA or tag, optionally semver) are first-class, and repackaging/publishing is optional for local iteration. When teams want governed releases, optional packaging formats include GitHub Release assets (with optional immutability), OCI artifacts, and ecosystem wrappers (npm/PyPI), all anchored by content digests for reproducibility and provenance. citeturn0search2turn6search0turn6search1turn2search5turn2search3

## Landscape research on existing prompt, eval, and packaging architectures

The current ecosystem is productive but fragmented. The dominant patterns are (a) CI-centric evaluation tools, (b) evaluation frameworks as libraries, (c) platform-centered prompt registries and dashboards, and (d) observability-first stacks that include eval but treat results as platform-state.

The table below summarizes what exists, the architectural center of gravity, and the gaps this doc addresses.

| System category | Representative systems | Architectural center | What tends to work well | What breaks for GitHub-native, low-friction teams |
|---|---|---|---|---|
| Config-driven eval runners + CI integrations | entity["organization","promptfoo","llm eval tool"] | Repo config files + a runner that posts results to PRs | Easy PR gating via before/after comparisons and CI automation. citeturn3search0turn3search4 | Often not package/consumption-first. Results may be ephemeral unless you build append-only artifacts, lineage, and promotion semantics around it. |
| Eval frameworks as code libraries | entity["company","OpenAI","ai research company"] Evals, DeepEval, Ragas, DSPy | Language/framework runtime is the primary abstraction | Powerful custom metrics, rich programmatic control, dataset formats like JSONL, and rubric/judge scoring. citeturn3search1turn3search5turn5search2turn5search3 | Couples teams to a runtime and evaluation contract; cross-language adoption can be hard; “control plane” becomes the framework and its conventions instead of GitHub releases and audit. |
| Prompt management + prompt registry platforms | entity["company","Langfuse","llm observability tool"], entity["company","PromptLayer","prompt management tool"], entity["company","Humanloop","prompt management platform"] | Central registry + SDK retrieval + UI versioning | Decouples prompt changes from app deploys; can support non-engineers; runtime retrieval plus caching patterns. citeturn3search2turn3search6turn3search3turn4search2 | External control plane becomes the “truth”, weakening Git-based review, diff, and release lineage; platform lifecycle churn is real (features deprecate). citeturn4search0 |
| Observability-first stacks with eval features | entity["company","Arize AI","ai observability company"] Phoenix, entity["company","Weights & Biases","ml tooling company"] Weave, TruLens | Traces/logs + evaluation within an instrumentation platform | Excellent debugging, tracing, and executor behavior (async concurrency, retries). citeturn5search4turn4search3turn5search1 | Results often live in platform state; you still need GitHub-native promotion policies, packaging, and pinning semantics if you want reproducible delivery gates. |

Key architectural takeaways from the landscape:

- CI-native eval runners are good at “PR feedback loops” but usually do not define a complete system of record for prompt assets as importable packages with promotion lineage. citeturn3search0turn3search4
- Frameworks are legitimate harness implementations, but they should not be the control plane because teams need multiple runtimes and evolving stacks; contract stability matters more than feature richness. citeturn3search1turn5search3
- Platform prompt registries solve “runtime hot swaps” and collaboration with non-engineers, but shift the source of truth away from GitHub; this complicates audit, diffs, and release gates unless you build a production-grade sync and governance layer. citeturn3search2turn3search3turn4search2
- Observability platforms solve “debug what happened” but don’t inherently solve “pin what shipped” in downstream applications, which is a packaging and promotion problem.

This proposal synthesizes the strengths (PR feedback loops, flexible harnesses, append-only run artifacts, and compatible packaging) into a GitHub-native system that stays portable.

## System thesis, principles, end states, non-goals, and users

**System thesis**

Prompts should be treated like versioned software assets with a declared interface, and eval evidence should be portable, reproducible, append-friendly, and gateable through GitHub’s existing review and release primitives. The system’s job is to define durable state, minimal contracts, and promotion semantics, not to become “the one framework”.

**Design principles**

- GitHub is the control plane. PRs and required status checks govern change; tags and releases govern distribution; audit logs govern accountability. citeturn0search0turn0search1turn0search6turn1search1
- Developer ergonomics dominates. Consumption must be simpler than authoring. Local iteration must not require publishing artifacts.
- Git-first consumption is first-class: local overrides and git ref pins (commit SHA, tag, optionally semver tags) are the default, not an escape hatch. npm and pip both support Git/VCS dependency forms, so the design can leverage existing developer muscle memory. citeturn6search0turn6search1
- BYO harness is mandatory. The system defines a minimal harness contract and durable artifact formats. Harnesses can be swapped without rewriting source-of-truth concepts.
- File-based durable state; stateless compute. Runners do work and emit artifacts; they do not own hidden state.
- Append-friendly immutable artifacts. Runs, reports, and promotions are records. Avoid in-place mutation.
- Explicit end states and transitions. Human checkpoints are clear and enforceable.
- Reproducibility is a feature. Content digests and provenance metadata are part of the system’s core output (not optional “enterprise extras”). SemVer rules apply only after declaring a public interface. citeturn2search0
- Optional packaging for governed releases. When teams want stronger distribution guarantees, use GitHub immutable releases, OCI digests, and SLSA-style provenance attestations. citeturn0search2turn2search5turn2search3

**Concrete end states**

The system is “working” when these outcomes are routine:

- A prompt revision can be traced from source commit → PR review → benchmark runs → regression decision → release tag/release asset → promotion record → delivery target receipt.
- Prompts can live inside an app repo or in a dedicated prompt repo without changing the conceptual model or consumption contract.
- Developers can consume prompts by pinning a commit SHA, tag, or semver tag in a consumption manifest, with local override for fast iteration.
- Any benchmark run has durable inputs and environment metadata recorded (prompt digest, dataset digest, evaluator digest, harness version, model IDs, sampling config) sufficient for replay within the constraints of non-determinism.
- Regression policies can gate merges and promotions via required status checks and protected branches. citeturn0search1turn0search5turn0search0
- Approved prompt versions are promoted via explicit promotion records; rollback is a promotion to a prior digest, not “edit in place”.
- Autonomous agents can operate safely because the repo contains machine-readable state; no hidden mutable database is required.

**Non-goals**

- Not a monolithic hosted eval platform. No required SaaS control plane.
- Not a single provider abstraction or agent framework.
- Not a prompt auto-optimizer (though harnesses may integrate optimization frameworks as an optional strategy). citeturn5search3
- Not a replacement for observability platforms; those can be harness-integrated sinks.
- Not a system that forces one repo topology; same-repo and separate-repo are equally supported.
- Not a system that makes publishing mandatory for development; git pins and local overrides are first-class.

**Users and use cases**

- Solo builders: want “prompt unit tests” and pinned prompts without adopting a platform.
- Product engineers: need PR gating, regression detection, and low-friction consumption.
- Platform teams: need reusable GitHub workflows, CODEOWNERS, and standardized artifact formats. citeturn1search0turn7search0
- Applied AI teams: need dataset discipline, judge calibration, multi-run variance tracking.
- Agencies: need portable packaging and clear release lineage across client repos.

## Core model: nouns, files, repo topology, and Black Hole Architecture mapping

### Core nouns and definitions

| Noun | Definition |
|---|---|
| Prompt spec | Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata. |
| Prompt package | Immutable bundle of prompt specs with a manifest and content digest; optionally associated with a semver version when released. |
| Provider artifact | A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper). |
| Dataset | Versioned evaluation cases (usually JSONL) with content digest and schema. |
| Evaluator | Scoring definition: deterministic checks, schema validation, rubric/judge config, or human review hooks. |
| Suite | Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds. |
| Harness adapter | Executable integration that can run suites and emit structured run artifacts. |
| Run request | Immutable “work order” file for running a suite against a revision. |
| Run artifact | Durable output of the run: manifest, scorecard, per-case records, raw artifact references, failures. |
| Scorecard | Normalized metrics summary for a run, including metric definitions and metric versioning. |
| Baseline | A named reference run/digest for regression comparison. |
| Regression report | Policy-evaluated candidate vs baseline comparison: pass/fail, warnings, evidence deltas. |
| Approval state | Machine-readable record that a revision/package passed required checks and human review. |
| Promotion record | Append-only record binding an approved digest/version to a channel and evidence links. |
| Delivery target | Declarative config describing how to sync an approved version to downstream systems. |
| Consumption manifest | App-side file declaring pins, overrides, and mappings from prompt IDs to usage. |

### Black Hole Architecture mapping

This system’s Black Hole mapping is intentionally strict.

**Durable state (source of truth, in Git):** prompt specs, datasets, evaluators, suites, harness adapter specs, regression policies, delivery target specs, consumption manifests.

**Stateless compute (workers):** GitHub Actions jobs, self-hosted runners, internal schedulers, notebooks, CLIs. Workers read run requests and emit run artifacts. Workers are replaceable and should be horizontally scalable.

**Append-friendly immutable artifacts (derived state):** run artifacts, regression reports, promotion records. These should be immutable records. Store small indexes in Git; store large raw outputs (transcripts, traces) in an open-ended artifact backend referenced by digest. GitHub Actions artifacts default to 90-day retention and should not be treated as the long-term archive. citeturn0search3turn0search21

**Human checkpoints:** PR review; explicit approvals for promotion and policy changes via CODEOWNERS and branch protection. citeturn1search0turn0search1

**Recovery and replay:** re-run a stored run request by resolving the same digested inputs and harness version. Allow for variance due to non-determinism and provider drift.

### Repo topology model and migration

This system supports three repo shapes without changing the conceptual model:

- **Same-repo:** prompts live in the app repo under `promptops/`.
- **Separate-repo:** prompts live in a dedicated repo; apps pin git refs or released artifacts.
- **Local-linked development:** developer uses a local override to a prompt repo checkout while CI resolves via git refs/digests.

Git submodules are a known alternative for embedding a repo at a pinned commit; they work but have operational friction and should be optional. citeturn6search10turn6search2

#### Topology tradeoffs table

| Topology | Strengths | Costs | When to choose |
|---|---|---|---|
| Same-repo | Simplest adoption; one PR can update code + prompts | Harder to share across many apps; release cadence tied to app | Most teams starting out; single product repo |
| Separate prompt repo | Clear reuse boundary; independent ownership and releases | Dependency update workflow; cross-repo coordination | Many apps share prompts; platform team owns prompts |
| Local-linked dev | Fast iteration without publishing; closer to real dev workflow | Needs a standardized override mechanism to prevent “works on my machine” | Separate repo + frequent co-development |

### Example repo trees

**Same-repo (prompts inside app repo)**

```text
.
├─ promptops/
│  ├─ prompts/            # prompt specs (source)
│  ├─ datasets/           # JSONL + manifests (source)
│  ├─ evaluators/         # evaluator specs (source)
│  ├─ suites/             # suites (source)
│  ├─ harnesses/          # harness adapter specs (source)
│  ├─ policies/           # regression + promotion policies (source)
│  ├─ delivery/           # delivery targets (source)
│  └─ manifests/
│     └─ consumption.yaml # app pins + overrides (source)
├─ derived-index/         # small append-friendly indices (optional)
│  ├─ baselines/
│  └─ promotions/
└─ .github/workflows/
```

**Separate prompt repo**

```text
.
├─ promptops/
│  ├─ prompts/
│  ├─ datasets/
│  ├─ evaluators/
│  ├─ suites/
│  ├─ harnesses/
│  ├─ policies/
│  └─ delivery/
├─ dist/                  # optional packaging output (not required for dev)
└─ .github/workflows/
```

**Artifacts branch (append-only indices)**
  
```text
# branch: promptops-artifacts
artifacts/
  runs/YYYY/MM/DD/<run_id>/
    run_manifest.json
    scorecard.json
    cases.jsonl
    artifact_refs.json
  reports/YYYY/MM/DD/<report_id>/
    regression_report.json
  promotions/YYYY/MM/DD/<promotion_id>/
    promotion_record.json
```

This “artifacts branch” pattern reduces merge conflicts and keeps derived artifacts out of the source-of-truth branch while remaining Git-native.

## GitHub primitives and why GitHub is the control plane

This system makes GitHub the control plane because GitHub already solves the core governance loop for software changes and provides APIs for automation feedback:

- **Status checks and required checks:** Branch protections can require checks to pass before merging to protected branches. citeturn0search1turn0search5turn0search0
- **Rulesets can require status checks for branches and tags:** Useful for enforcing policies across repos and environments. citeturn0search9
- **Checks API:** You can create check runs via GitHub Apps to provide rich feedback and annotations in PRs; write access for checks is limited to GitHub Apps (not OAuth apps). citeturn1search2turn1search6turn7search17
- **Commit Status API:** Useful when you’re not building a GitHub App; supports creating statuses per SHA, with documented limits. citeturn7search1
- **CODEOWNERS:** Define who must review which parts of the repo (prompts, policies, harness specs). citeturn1search0
- **Tags and releases:** Releases are based on Git tags and mark points in history; releases can carry assets. citeturn0search6turn0search20
- **Immutable releases:** Assets and the associated tag cannot be changed after publication, hardening distribution semantics for release assets. citeturn0search2turn0search13
- **Actions artifacts retention:** Default 90-day retention; configurable. This matters for where you store long-lived run outputs. citeturn0search3turn0search21
- **Audit logs:** Org admins can review actions, including who did what and when. citeturn1search1turn1search12
- **Reusable workflows (`workflow_call`):** Lets platform teams standardize PromptOps workflows across many repos. citeturn7search0turn7search8

**Design implication**

GitHub owns the canonical collaboration and governance loop. The PromptOps system should not build a competing “prompt versioning database”. Instead, it should encode state transitions as files, checks, and tags, and treat dashboards as derived views.

## Prompt packaging and consumption model optimized for Git-first ergonomics

### The core posture

Repackaging and publishing is optional for local iteration.

The default developer loop is:

- edit prompt file(s)
- run local smoke suite via your harness
- open PR
- CI runs suites and posts regression report
- merge if policy passes
- optionally release and promote

Publishing artifacts (OCI/npm/PyPI/release asset) is a governed release behavior, not required for day-to-day prompt edits.

### Git-first resolution as a first-class primitive

The system uses a consumption manifest and a resolver with this precedence:

1) **Local override** (local path)  
2) **Workspace path** (same-repo prompts under `promptops/`)  
3) **Git ref** (tag or commit SHA)  
4) **Packaged artifact** (release asset / OCI digest / registry wrapper)

This is implementable today because standard ecosystems already support Git-based dependencies:

- npm can install from git URLs pinned by `#<commit-ish>` and can resolve tags using `#semver:<range>`. citeturn6search0
- pip supports VCS requirements in the form `ProjectName @ VCS_URL` and supports multiple git URL schemes. citeturn6search1

### Package identity: digest-first, semver-optional

- **Content digests are the canonical identity.** Digests are used for reproducibility and to guarantee “what exactly ran” and “what exactly shipped”.
- **SemVer is supported when (and only when) the prompt package declares a public interface.** SemVer explicitly requires that software declare a public API. citeturn2search0  
  For prompt packages, the “public API” should mean: prompt ID, variables schema, output contract/schema, and (if relevant) tool schema/contract.

### Governed release packaging options

When teams want governed distribution, allow more structure without sacrificing Git-first dev ergonomics.

| Packaging mode | Pinning surface | Strengths | Costs | Best use |
|---|---|---|---|---|
| Git ref (tag/SHA) | `git+...#<sha>` or tag in manifest | Zero publishing; simplest | Requires git access; caching matters | Dev, early adoption, internal use |
| GitHub Release asset | Release tag + asset digest | Tag lineage; easy download; can be immutable | Not natively digest-addressed unless you add digests | Governed releases, low infra |
| OCI artifact | `name@sha256:...` | Digest-addressed; supports tag + digest; supports associated artifacts/referrers | Registry complexity | Org-wide artifact distribution |
| npm/PyPI wrapper | semver in ecosystem | Best app ergonomics | Publishing pipeline overhead | Mature orgs, broad consumer base |

For OCI, the distribution spec explicitly defines that a manifest reference must be either a digest or a tag, which maps cleanly to “pin by digest for immutability” and “use tags for human-friendly references”. citeturn2search5

OCI is operated by entity["organization","Open Container Initiative","container standards org"] as an open governance structure creating open standards. citeturn2search9

### Provenance, signing, and supply-chain posture

This system should support provenance without requiring it in phase one:

- SLSA provenance defines provenance as an attestation that a builder produced artifacts by executing an invocation using materials (inputs). citeturn2search3
- GitHub provides artifact attestations to establish build provenance for artifacts produced in Actions, for consumers to verify where and how software was built. citeturn6search3
- GitHub immutable releases harden release asset distribution by preventing changes after publication. citeturn0search2

Practical recommendation: start by recording digests and workflow run IDs in manifests; add attestations and signature verification later as an optional “governed release profile”.

## BYO harnesses, eval discipline, regressions, delivery, walkthroughs, agents, and build plan

### Minimal BYO harness contract

The system supports any harness, including scripts, notebooks, internal schedulers, or wrappers around existing tools (such as promptfoo or a framework like OpenAI Evals). citeturn3search0turn3search5

**Contract: run request in → run artifact out**

**Inputs (to harness):**
- `run_request.json` (or YAML): suite ID, revision ref (SHA/tag/digest), model matrix, trials, budgets, timeouts, evaluator refs, artifact backend config.
- Resolved prompt package or instructions for resolver to materialize it.
- Output directory for artifacts.

**Harness must:**
- Resolve revision to a concrete prompt package digest.
- Execute suite across datasets and model matrix, with trials if configured.
- Apply evaluators and produce metrics.
- Emit a structured run artifact directory.
- Attach raw transcripts/traces/logs by reference and digest.
- Record environment metadata sufficient for reproduction attempts.

**Required outputs:**
- `run_manifest.json`: input refs, resolved digests, timestamps, harness version, model IDs, sampling config, environment, status.
- `scorecard.json`: normalized metrics, metric definitions, metric versioning, variance if trials.
- `cases.jsonl`: per-case records with stable case IDs, per-trial outputs, evaluator outputs, pointers to raw text/traces.
- `artifact_refs.json`: URIs + digests to raw artifacts.
- `failures.json`: structured failures if any.

This thin contract is deliberate: it prevents lock-in to any single evaluation framework while allowing frameworks to be “just another harness”.

### Benchmarking and evaluation best practices

This section is intentionally opinionated because weak eval discipline produces false confidence.

**Treat eval as a measurement system, not a dashboard**

- Systematically catch regressions and compare prompt changes as part of shipping confidence, not post-hoc debugging.
- Retain raw outputs for audit and diagnosis; do not rely only on aggregated scores. This is consistent with practical eval guidance that emphasizes inspecting transcripts to validate graders and understand failures. citeturn5search0

**Suite tiers (recommended default)**

| Tier | Purpose | Size/cost | Trigger | Output expectation |
|---|---|---|---|---|
| Smoke | Fast sanity checks | Small | Local + every PR | Deterministic-ish, quick pass/fail |
| Regression | Protect known failure modes | Medium | PRs that change prompts/policies | Evidence-heavy regression report |
| Full | Broader coverage | Large | Nightly / on-demand | Trend analysis, drift detection |
| Release candidate | Ship gate | Large | Pre-release / promotion to prod | Highest rigor, human signoff |

**Dataset hygiene and versioning**
- Use append-friendly JSONL with stable case IDs.
- Version datasets independently from prompts; treat dataset edits as new versions with new digests so comparability remains legible.

**Judge calibration and bias**
- If using judge models, version the judge prompt and judge model identifier; treat judge config as part of the evaluator spec. This aligns with the reality that judge behavior can drift.
- Prefer deterministic checks when possible (schema validation, exact match for structured outputs).

**Sample size, variance, and flakiness**
- Support trials and record variance; regression policies should be variance-aware.
- Quarantine flaky cases and track their flake rate; do not let flakiness silently pass as “random noise”.

**Prevent overfitting**
- Maintain holdout sets for release candidates.
- Promote regressions from production incidents into a “never again” regression suite.

### Policy-driven regression detection model

Regression detection is a deterministic function of:

- candidate scorecard + baseline scorecard + policy spec → regression report.

**Baseline selection**
- Default baseline should be “prod current” (from promotion record) or “last release candidate passing run”.
- Baseline references should resolve to immutable run IDs/digests, not “latest”.

**Policy semantics**
- Per-metric rules: absolute floors, allowed deltas, and directionality.
- Hard blockers vs warnings: blockers fail checks; warnings require signoff.
- Tradeoff surfacing: explicitly show quality vs cost vs latency changes in the regression report.

**GitHub gating**
- Regression policy results should be surfaced as a required status check for protected branches. Branch protection can require passing checks before merge. citeturn0search1turn0search5

### Delivery and promotion model

Promotion is a first-class transition that binds immutable prompt artifacts to channels and delivery targets.

**Key rule:** production never runs “floating prompt versions” unless you explicitly decide to. Production pins digests.

**Abstract delivery targets**
- PR to downstream app repo updating `consumption.yaml`.
- Publish OCI digest to an internal registry namespace.
- Sync a config store used by edge/runtime systems.
- Post a signed “release descriptor” to an internal API.

**Key point:** the system does not assume a hosted platform is the center. Delivery is adapters.

#### Promotion and delivery flow diagram

```mermaid
flowchart TD
  A[Author prompt change] --> B[Local smoke eval via harness]
  B --> C[Open PR]
  C --> D[CI creates run_request for required suites]
  D --> E[Stateless worker runs harness]
  E --> F[Run artifact emitted: manifest + scorecard + cases]
  F --> G[Policy engine produces regression report]
  G -->|fail| H[Blocking check fails; iterate]
  G -->|pass| I[Required checks green]
  I --> J[Human review + CODEOWNERS]
  J --> K[Merge]
  K --> L[Optional: release candidate run]
  L --> M[Tag + Release (optional: immutable)]
  M --> N[Promotion record appended]
  N --> O[Delivery worker syncs to targets]
  O --> P[Downstream apps pin digest/tag]
  P --> Q[Rollback = promote prior digest]
```

Releases are based on Git tags. citeturn0search6  
Immutable releases can prevent release assets and tags from being modified after publication. citeturn0search2

### Lifecycle walkthroughs

**Walkthrough: low-friction prompt edit with no publishing**
A developer edits a prompt spec in the app repo and runs a smoke suite locally using their harness. They open a PR, and CI triggers regression suites. A regression report check is posted; if it fails, merge is blocked on the protected branch by required status checks. Publishing is not involved. citeturn0search1turn0search0

**Walkthrough: separate prompt repo with commit pin consumption**
A prompt repo releases no formal packages yet. The consuming app pins a commit SHA in its consumption manifest and means “ship exactly this”. Local-linked dev is enabled by a local override path. npm and pip both support Git/VCS dependency forms, so language-specific wrappers remain optional. citeturn6search0turn6search1

**Walkthrough: release candidate and governed promotion**
After regression suites pass on main, the system triggers a release-candidate run. A tag and GitHub Release are created, optionally using immutable releases for stronger supply-chain posture. The promotion record binds release digest to “prod”, then a delivery worker opens PRs to update downstream apps’ consumption manifests. citeturn0search2turn0search6

**Walkthrough: multi-harness comparisons without changing system nouns**
The team runs the same suite through two harness adapters: a Python harness and an internal scheduler harness. The run artifacts are comparable because the contract is the same. Only the `harness_version` and environment metadata differ. The regression policy applies identically.

**Walkthrough: audit replay**
An incident requires replay. The team retrieves a past run request and resolved digests, re-runs the harness, and compares variance. This is only possible because artifacts are durable and content-addressed, rather than buried in an ephemeral CI log with 90-day retention. citeturn0search3turn0search21

### Agentic workflow compatibility and safe agent interactions

Agents can safely operate when state is explicit and file-based:

- Agents propose prompt edits by opening PRs that change prompt specs and suites.
- Agents generate run requests and trigger workflows.
- Agents summarize regression reports and attach evidence to PR discussions.
- Agents prepare promotion record PRs, but humans approve promotions.

If you want richer PR feedback, checks APIs allow GitHub Apps to create check runs and annotate commits. citeturn1search2turn1search6  
Reusable workflows allow platform teams to standardize automation across many repos. citeturn7search0turn7search8

### Risks and mitigations

| Risk | Failure mode | Mitigation |
|---|---|---|
| Benchmark gaming | Teams optimize for benchmark score | Holdouts, incident-driven regression suites, require evidence cases |
| False confidence | Narrow suites miss real failures | Tiered suites + capability tagging + forcing release-candidate gates |
| Flaky evals | Noise causes churn or hides regressions | Trials + variance-aware gating + flake quarantine |
| Artifact sprawl | Repo becomes unusable | Store only indices in Git; raw artifacts in backend; enforce retention |
| Platform/tool churn | Features disappear (vendor churn is real) | Keep core: files + git refs + digests; harnesses are adapters. Feature deprecations in platforms are documented realities. citeturn4search0 |
| Supply-chain tampering | Modified release assets or tags | Immutable releases; attestations; digest pinning. citeturn0search2turn6search3 |
| Overgrown harness contract | Lock-in by another name | Keep contract minimal; treat harnesses as replaceable compute |
| Confusing metrics | Teams don’t know what “score” means | Metric definitions and versions embedded in scorecard schema |

### Phased build plan

| Phase | What to build | Value unlocked |
|---|---|---|
| Spec + validation | JSON/YAML schemas and validators for core files | Agents and humans share a stable machine-readable protocol |
| Git-first resolver + minimal runtime | Resolve prompts from workspace, local override, git refs | Low-friction consumption without publishing |
| Deterministic digest tooling | Canonicalization + digests for prompts/datasets | Reproducibility and meaningful lineage |
| Harness adapter runner | Run request → harness → run artifact | BYO compute becomes real |
| Regression policy engine | Baselines + blockers/warnings + diff reports | Merge gating on real quality evidence |
| GitHub integration | Checks/status reporting, reusable workflows, CODEOWNERS patterns | Org-wide PromptOps standardization. citeturn1search2turn7search0turn1search0 |
| Release + promotion | Tags/releases, immutable release option, promotion records | Governed distribution and rollback. citeturn0search6turn0search2 |
| Optional hardening | OCI artifacts, attestations, verification UX | Supply-chain integrity and scalable distribution. citeturn2search5turn2search3 |

### Open questions

- Which artifact backend(s) are the default recommendation for long-lived raw outputs (OCI registry vs object storage vs release assets), given Actions artifacts are 90-day retention by default? citeturn0search3turn0search21
- What is the canonical “public interface” for semver decisions (variable schema, output schema, tool contract)?
- How strict should deterministic packaging be (canonical JSON ordering, YAML normalization)?
- How will you model evaluator evolution and metric versioning to preserve long-term comparability?
- How will you represent sensitive datasets (PII) while maintaining digest-based reproducibility (encrypted datasets, access policies, or synthetic surrogates)?

### Final recommendation

Build PromptOps as a GitHub-native protocol and workflow layer, not a platform. Make Git-first consumption and local overrides first-class so developers can iterate without publishing artifacts. Use content digests as the primary identity for reproducibility. Keep the harness contract thin but non-negotiable. Store derived artifacts as append-only records; do not rely on ephemeral CI logs. Use GitHub required checks and branch protections to gate merges and promotions, and use tags/releases (optionally immutable) as the release boundary. citeturn0search0turn0search1turn0search6turn0search2

## Public prompt library registry v2 primitive with single-custodian model

This section addresses a v2 primitive: a public prompt library/registry that hides Git/GitHub behind a custodian account and exposes a public app/SDK, while still preserving Git-first developer ergonomics.

### What “single-custodian” means

A single-custodian registry is a public service that:

- accepts prompt package submissions (as bundles, OCI artifacts, or signed manifests),
- runs moderation and policy checks centrally,
- publishes approved artifacts under a custodian namespace,
- exposes public APIs and SDKs for discovery and consumption,
- maintains append-only provenance and moderation logs.

Git is still used internally for versioned review and audit, but the public interface is not “go to GitHub and browse repos”. It’s “query a registry and install prompts”.

### Registry custody model comparison

| Model | Who can publish canonical names | Governance | Strengths | Weaknesses |
|---|---|---|---|---|
| Single custodian (one canonical registry) | Custodian controls namespace and acceptance | Central policy + moderation | Discoverability; consistent quality gates; strong dedupe; easier public SDK story | Trust concentration; moderation load; legal exposure; single point of failure |
| Federated (multiple custodians with shared protocol) | Multiple registries with peering/mirrors | Distributed governance | Avoids single point of failure; local policies | Fragmented discovery unless well-designed; cross-registry trust is hard |
| Fully decentralized (content-addressed swarm) | Anyone publishes by digest | Emergent / minimal | Strong censorship resistance; no gatekeeper | Very hard moderation; weak canonical naming; poor UX for most dev teams |

Pragmatic product recommendation for v2: start with a single custodian to solve discoverability, naming, quality gates, and SDK ergonomics, then add federation/mirrors once the protocol is stable.

### How the custodian model maps to Black Hole Architecture

Durable state (canonical):

- Append-only registry metadata store: package manifests, digests, signatures/attestations, moderation decisions, vulnerability flags, deprecation notices.
- Versioned source submissions stored as immutable bundles, referenced by digest.

Stateless compute:

- Submission validation workers
- Moderation assistance workers (rules + models + human review queues)
- Indexing/search workers
- Promotion and mirroring workers

Append-only artifacts:

- Submission records
- Moderation decision records
- Provenance attestations
- Deprecation and takedown records
- Mirror sync receipts

Human checkpoints:

- Moderation approval for public listing
- Policy exceptions
- Emergency takedown decisions

Replay and recovery:

- Recompute indices from stored manifests and artifacts. The registry’s “truth” is the append-only log + content store.

### Public APIs and SDK surface area

The public API should be minimal and stable:

- `GET /packages?query=...` (search, tags, compatibility filters)
- `GET /packages/{name}` (metadata, versions, digests, policy flags)
- `GET /packages/{name}/versions/{ref}` (resolve tag/semver to digest)
- `GET /artifacts/{digest}` (fetch artifact or redirect)
- `GET /provenance/{digest}` (attestations, build provenance, signatures)
- `POST /publish` (submit package, metadata, proof of ownership, signatures)

SDKs should support:

- Resolve by semver/tag/SHA-like ref to a digest, then fetch.
- Local caching and offline fallback (mirroring the caching posture that platform prompt registries use for low-latency retrieval). citeturn3search6
- Verify signatures/attestations optionally.
- Emit a consumption manifest entry for Git-first teams (so SDK is additive, not mandatory).

### Publishing, provenance, and signing

**Publishing pipeline**
- Author submits a package bundle or OCI artifact.
- Registry computes/validates content digest; checks schema validity; runs malware and policy scans.
- Registry verifies provenance attestations if provided; otherwise marks provenance as “unsigned/unverified”.

This design leans on established supply-chain ideas:
- SLSA provenance describes builder/invocation/materials, explicitly stating that you ultimately trust the builder to record provenance correctly. citeturn2search3
- OCI distribution supports pulling manifests by tag or digest, enabling content-addressed pinning and verifiable resolution. citeturn2search5
- GitHub artifact attestations can be a default mechanism for provenance in early phases if the custodian uses GitHub Actions as its build system. citeturn6search3

### Moderation, governance, and legal/ToU considerations

A public registry is a content platform as much as a developer tool. You need explicit governance and moderation.

- GitHub’s Terms of Service and Acceptable Use Policies are an example of the types of content and conduct constraints a platform must define and enforce (safety, IP, privacy, authenticity). citeturn8search4turn8search0
- GitHub also publishes community guidelines describing investigation of abuse reports and moderation of public content, reinforcing that public hosting requires moderation procedures. citeturn8search8

Concrete recommendations for a custodian registry:

- **Custody and trust:** Be explicit that the custodian is a trusted publisher for canonical names. Provide verifiable digests and provenance data so users can make informed trust choices.
- **Governance:** Publish a transparent policy for naming, ownership disputes, takedown appeals, and deprecation.
- **Moderation:** Require (a) automated scanning (schema validation, secrets detection, obvious policy checks), (b) community reporting, and (c) a human escalation path for high-risk content.
- **Mirrors:** Support read-only mirrors from the start (even if unofficial) by making artifacts content-addressable and easy to sync. Federation becomes possible later if the protocol is stable.
- **Keep Git-first ergonomics:** Even with a public app/SDK, preserve git-based workflows by allowing “export to GitHub repo” and “install by digest pinned in a manifest” so developers can keep their normal review and deployment loop.

### Public registry flow diagram

```mermaid
flowchart TD
  A[Publisher creates prompt package bundle] --> B[Compute digest + schema validate]
  B --> C[Submit to custodian /publish API]
  C --> D[Automated checks: policy + malware + schema]
  D -->|needs review| E[Human moderation checkpoint]
  D -->|pass| F[Accept submission record (append-only)]
  E -->|approve| F
  E -->|reject| G[Reject record + reasons (append-only)]
  F --> H[Publish under canonical name]
  H --> I[Attach provenance/signatures]
  H --> J[Update search index]
  J --> K[Public app + SDK resolve name/ref to digest]
  K --> L[Consumers pin digest or semver in manifest]
  L --> M[Optional mirrors sync by digest]
```

### Rollout plan for “de facto public prompt library and benchmark suite”

A credible rollout plan should prioritize developer ergonomics and trust-building, not UI polish.

**Phase 1: Protocol and reference implementation**
- Publish the file spec (prompt specs, suite specs, run artifacts, digests).
- Provide a reference CLI that resolves prompts using local overrides and git refs (commit/tag), and emits a consumption manifest entry.

**Phase 2: Public library as a GitHub-native corpus**
- Host canonical prompt packs as GitHub repos under custodian org initially to bootstrap trust and transparency.
- Use releases (optionally immutable) to publish bundles and attach provenance evidence. citeturn0search6turn0search2

**Phase 3: Registry API as a derived view**
- Build a registry that indexes the GitHub-hosted corpus and exposes public APIs/SDKs.
- Keep the “export to Git repo” path first-class so Git-first teams keep their workflow.

**Phase 4: Moderation and governance hardening**
- Publish Acceptable Use and deprecation policies for the registry, modeled after established platform patterns (ownership disputes, takedowns, appeals). citeturn8search0turn8search4turn8search8
- Add provenance requirements for “trusted publisher” badges.

**Phase 5: Federation and mirrors**
- Specify mirror protocol (sync by digest) and optional federation (multiple custodians).
- Avoid premature decentralization; solve naming, trust, and moderation first.

## Appendices

**A) One-paragraph product pitch**  
Black Hole PromptOps is a GitHub-native PromptOps layer that lets teams ship prompts with the same discipline as code: prompts and eval specs live as versioned files; bring-your-own harnesses execute suites; results are durable, append-only artifacts; regressions gate merges and promotions via required status checks; and approved prompt packages can be promoted to delivery targets with safe rollback. Local iteration stays frictionless because repackaging/publishing is optional and Git-first pins plus local overrides are the default.

**B) Ten design decisions to lock early (recommended)**

| Decision | Why it must be early |
|---|---|
| Prompt spec schema and templating rules | Prevents ecosystem fragmentation and breaking changes |
| Stable prompt IDs and rename policy | Enables cross-repo moves without semantic breakage |
| Consumption manifest schema + resolver precedence | Defines ergonomics and prevents “works locally only” bugs |
| Canonical digest computation and normalization | Backbone of reproducibility and lineage |
| Run artifact schema (manifest/scorecard/cases) | Enables regression engine and historical comparability |
| Metric naming + metric versioning rules | Prevents silent semantic drift in scorecards |
| Suite spec model (matrix, trials, budgets) | Controls cost and determinism tradeoffs |
| Regression policy language | Determines whether gating is trusted or ignored |
| Promotion record semantics and channels | Enables stable delivery and rollback |
| Artifact storage strategy (open-ended but specified) | Prevents accidental reliance on 90-day retention artifacts. citeturn0search3 |

**C) Ten mistakes to avoid**

| Mistake | Consequence |
|---|---|
| Mandating publishing for every prompt tweak | Developers bypass the system |
| Coupling core concepts to one eval framework | Lock-in and churn pain |
| Letting consumption require the authoring stack | bloated runtime and poor adoption |
| Treating CI logs as the archive | Loss of auditability after retention expires. citeturn0search3 |
| Ignoring variance and trials | Flaky gates and false confidence |
| Using a single aggregate score as truth | Hidden regressions and safety failures |
| Not versioning evaluator logic | Historical comparisons become meaningless |
| Putting derived artifacts on main branch | Merge conflicts and repo bloat |
| “Floating latest prompt” in production | No rollback safety and unclear lineage |
| Building a UI-first platform before the spec | Protocol instability and ecosystem lock-in |

**D) Minimal viable internal schema inventory**

| File type | One-line explanation |
|---|---|
| `prompt.yaml` | Prompt spec with stable ID, vars schema, output contract, metadata |
| `dataset_manifest.yaml` | Dataset identity, schema version, digest, provenance |
| `dataset.jsonl` | Append-friendly test cases with stable `case_id`s |
| `evaluator.yaml` | Scoring definition; judge config is versioned here |
| `suite.yaml` | Benchmark suite: datasets, evaluators, model matrix, trials, budgets |
| `harness_adapter.yaml` | How to invoke harness + capabilities + required env vars |
| `run_request.json` | Immutable instruction: suite + revision + config |
| `run_manifest.json` | Resolved digests + model IDs + env metadata + status |
| `scorecard.json` | Normalized metrics + metric versions + variance |
| `cases.jsonl` | Per-case results and pointers to raw outputs |
| `artifact_refs.json` | URIs + digests to large raw artifacts |
| `regression_policy.yaml` | Baseline rules + thresholds + blockers/warnings |
| `regression_report.json` | Candidate vs baseline outcome + evidence |
| `promotion_record.json` | Append-only promotion binding digest/version to channel |
| `delivery_target.yaml` | Declarative target sync config |
| `consumption.yaml` | App-side pins, overrides, and prompt-ID mappings |

**E) Repo build handoff for an autonomous coding agent**

Build in this order:

1) Define schemas + validators for prompt spec, suite, run request, run manifest, scorecard, regression policy.  
2) Implement the resolver: local override → workspace → git ref retrieval (tag/SHA) → packaged artifact.  
3) Implement deterministic digest computation for prompts and datasets (canonicalization rules).  
4) Implement minimal consumption runtime: resolve prompt ID → render template → return structured prompt + metadata.  
5) Implement runner shim: invoke harness adapter with run request; collect run artifact directory.  
6) Implement regression engine: compare scorecards, emit regression report, and publish a GitHub check/status result via the appropriate API surface. citeturn1search2turn7search1

**F) Topology recommendation matrix**

| Choose this when | Same-repo | Separate prompt repo | Local-linked dev |
|---|---:|---:|---:|
| You want fastest adoption | Strong | Medium | Medium |
| Prompts are reused across apps | Medium | Strong | Strong |
| You need independent releases/ownership | Weak | Strong | Medium |
| You must avoid publishing per tweak | Strong | Strong (git pins) | Strong |
| Your org wants clear gates and lineage | Medium | Strong | Medium |
| Your team can standardize local overrides | Not needed | Helpful | Required |
