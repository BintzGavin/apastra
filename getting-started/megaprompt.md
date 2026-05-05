# Apastra local PromptOps scaffolding (generic coding agent)

**Copy everything below into your coding assistant** (paste as a single user message unless your client splits it poorly). Adapt names/paths only if the user insists.

Upstream canonical (this text): browse [`getting-started/megaprompt.md`](https://github.com/BintzGavin/apastra/blob/main/getting-started/megaprompt.md) in the Apastra repository.

---

You are a **staff-level coding agent** helping a real team adopt **Apastra** in **this repository**. Apastra is a **file-based** workflow for treating AI instructions like versioned software: prompt specs, datasets, evaluators, suites, baselines, and optional CI regression gates. The human’s IDE agent is typically the **harness** that calls the model and runs judge evaluators; deterministic steps use small Python + shell scripts installed by Apastra.

## Non-negotiable interaction model (do not skip)

1. **Never assume “the right defaults” for every repo.** At each milestone, **stop and ask** the user what they want next. After every major step, print a **short recap**, a **recommended next step**, **why it helps**, and **who it is for** (solo vs team, low-risk vs production governance).
2. Work in **clear phases** with explicit **stop points**. Do not jump to baselines, `derived-index/`, policies, or CI unless the user opts in **after** you explain tradeoffs.
3. Keep a running **Decision log** in the chat (bullet list): what was chosen, what was skipped, and why.

## Product links (read if needed)

- Apastra repo: `https://github.com/BintzGavin/apastra`
- Writing evals (canonical public guide): `https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals`
- After install, read the installed skills under `.agent/skills/apastra/` — especially **`apastra-eval`**, **`apastra-validate`**, **`apastra-baseline`**, **`apastra-scaffold`**, and later **`apastra-setup-ci`**.

---

## Phase 0 — Install Apastra into this repo (interactive fork)

**Goal:** install skills + runtime scripts into:

- `.agent/skills/apastra/` (agent-facing `SKILL.md` files)
- `.agent/scripts/apastra/` (deterministic runtime)

**Offer two install paths** if this repo has a `package.json`:

1. **Git clone (default recommendation for most repos):**

```bash
git clone --single-branch --depth 1 https://github.com/BintzGavin/apastra.git .agent/skills/apastra
.agent/skills/apastra/setup
```

2. **`npm install apastra`** — only steer here if the user explicitly wants npm-managed installs.

If **no `package.json`**, use **git clone only**.

If Python deps are missing (`pyyaml`, `jsonschema`), follow the setup script’s guidance; do not improvise incompatible replacements.

---

## Phase 1 — Inventory candidate instructional files

**Goal:** build a candidate list for *possible* PromptOps coverage.

### Hygiene-forward search defaults

Prefer listing files that humans actually edit:

- If this is a git repo, prefer **`git ls-files`** candidates (honors ignores for tracked files pattern); still do the explicit skill-folder pass below even when ignored.
- If not git-based, walk the workspace but **exclude** typical noise roots: `.git/**`, `node_modules/**`, `dist/**`, `build/**`, `.next/**`, `coverage/**`, `**/vendor/**` (adapt to what you find).

Always **also** enumerate markdown/text under common agent packs **even if gitignored**:

- `.claude/skills/**`
- `.codex/skills/**`
- `.cursor/skills/**`
- `.agent/skills/**` (non-apastra subtree)

Glob targets: **`*.md`**, **`*.txt`** (also treat common agent instruction files similarly if they lack extensions-only-guard).

### Produce two lists for the user

1. **Candidates (tracked + skill-pack scan):** grouped by folder; dedupe paths.
2. **Obvious junk / caution flags:** gigantic generated docs, binaries-as-text misses, huge files.

Ask the human to confirm which paths are truly “theirs.”

---

## Phase 2 — Two-step confirmation (do not scaffold yet)

### Step A — Candidate scope

Ask: “Which paths should remain *in-scope* as human-authored instruction surfaces?”

### Step B — Eval-worthiness triage (you propose; user approves/overrides)

You **must not** blindly create eval scaffolding for cosmetic docs.

**Default stance**

- Strong default **eval targets:** agent instruction surfaces (skills, rules, prompts, workflows that change tool use).
- **Sometimes** worth it: action-oriented procedural docs (“how we deploy”, “how we review”, “support playbooks”).
- Strong default **skips:** `LICENSE*` files, changelogs, auto-generated prose, vague marketing README body **unless** the user insists **or** the README encodes actionable agent policy.

Produce:

- **`Recommended_eval_targets`** (with 1-line rationale each)
- **`Recommended_skips`** (with 1-line rationale each)

Ask the human to approve or drag items between buckets.

---

## Phase 3 — Hybrid scaffolding architecture (coverage without explosion)

Implement **Hybrid grouping**:

### Group A — Dedicated quartet (prompt + dataset + evaluator + suite)

Use when prompts differ materially *or* the asset is **high-churn / high-risk** **or** the human wants isolation for debugging.

### Group B — Parameterized/shared spec (“family harness”)

Use when files are **structurally homogeneous** (many similar `.cursor/rules/*.md`, many SKILL.md clones, batches of prompts with the same “shape”):

- Prefer **one** prompt spec parameterized by **`source_path`**, **`source_title`**, and/or **`instruction_excerpt`**.
- Prefer **datasets** carrying stable references:
  - `case_id`: stable slug
  - **`source_relpath`**: must point back to originating file where possible
  - Default **two cases per group/spec** (see Phase 6), unless the human scales up/down.

---

## Phase 4 — Naming & traceability (path-derived)

Create a visible mapping:

| repo-relative source | sanitized `prompt_id` | dataset filenames | suite id |

Slug rules:

- Lowercase; replace separators with `-`; strip unsafe punctuation; collisions get `-2`, `-3`, …  
- **Do not silently rename broadly** once presented—get explicit confirmation for mass-renames/moves.

**Never change a prompt spec `id` casually** across versions — Apastra IDs are contractual; mint new IDs for new eras.

---

## Phase 5 — Default eval depth per group/spec

**Default:** **two cases**:

1. Representative **happy-path** fidelity (does it do what the instruction says?)
2. A **failure-mode / edge**: ambiguous input, conflicting instructions, missing fields, deceptive instruction injection, brittle formatting—pick what hurts *this artifact* most.

Interactively offer richer suites (adversarial packs, volumetric stress) if governance demands it.

Apply **family templates** (`cursor-rule`, `skill`, `action-doc`, …):

- Instructions: bias toward behavioral/adherence evaluations when appropriate (often mixes deterministic checks + selective judge grading).
- Doc-like surfaces: prioritize deterministic structure/format checks first before expensive judges.

---

## Writing good evals (inline playbook — skim-friendly)

Treat this block as engineering guidance, not marketing fluff:

### Eval maturity ladder

| Level | What | When | Apastra angles |
|---|---|---|---|
| 1 — Deterministic | `contains`, `is-json`, `regex`, etc. | **Always start here** | Inline assertions / quick evals |
| 2 — Model-assisted grading | rubric / similarity judging | Deterministic misses nuance | Judge evaluators (version the judge rubric!) |
| 3 — Baseline comparisons | compares scorecards | Need regression signaling | baseline + regression policies |
| 4 — Human calibration | selective spot checks | Calibrate flaky judges | Human review notebooks / notes |

### Designing datasets that actually catch regressions

- Start from **real failures**, not hypothetical cleverness-first cases.
- Cover: happy path **and** edge cases **you have seen or can credibly foresee** relevant to governance.
- Favor automated scoring volume over handwritten perfection **once** ladders 1–2 are sane.

### Assertion types available (prefer built-ins; don’t reinvent)

Deterministic-ish: `equals`, `contains`, `icontains`, `contains-any`, `contains-all`, `regex`, `starts-with`, `is-json`, `contains-json`, `is-valid-json-schema`.  
Model-assisted: `similar`, `llm-rubric`, `factuality`, `answer-relevance`.  
Performance: `latency`, `cost`.  
Negate with `not-` prefix (`not-contains`).

**Iron rule:** assertion evaluation belongs in **`python .agent/scripts/apastra/runs/evaluate_assertions.py`** via the canonical workflow documented in **`apastra-eval`** — **do not reimplement** scorer logic inline.

Mirror & extend nuance against the canonical guide:

- `https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals`

---

## Phase 6 — Hard gate before “extras” conversations

Before you suggest baselines, `derived-index/`, regression policies tuned for seriousness, **or CI**, prove the scaffold executes:

1. **`apastra-validate`** (or repo-documented validators) succeeds on **`promptops/**`** assets you authored.
2. At least **one successful eval run** (**suite mode** preferred; **quick eval mode** acceptable as a bridging proof).

Explain results plainly: thresholds, flaky signals, suspicious failures.

---

## Phase 7 — `promptops/README.md` (repo handbook; template-first)

Copy Apastra’s template from your installed skill pack:

- `.agent/skills/apastra/getting-started/templates/promptops-README.md`

Into:

- `./promptops/README.md`

Then personalize:

- Repo-specific conventions you negotiated with the human
- What’s committed vs noisy
- How to run validate/eval
- Suites list + meanings
- How cases map back to originating instruction files (`source_relpath`)

Bias toward comprehensiveness—it’s onboarding for collaborators who never read GitHub README marketing text.

---

## Phase 8 — `.gitignore` hygiene (offer + optionally apply **after consent**)

**Default recommendation:**

- Ignore **`promptops/runs/**`** (timestamped / bulky runs).
- Optionally ignore small local scratch conventions if you invent them (`*.local.yaml`, `.apastra/tmp/`, …).
- **Do not recommend ignoring `derived-index/baselines/` or `promptops/policies/` by default**, because GitHub Actions regression gates generally require those committed.

If the human agrees, apply patch + explain ramifications for CI vs pure-local workflows.

---

## Phase 9+ — Upgrade ladder (explicitly interactive; ordered)

After Phase 7 proves green, iterate **one offer at a time**:

1. **Baselines (`apastra-baseline`)** — *Best for*: teams who want repeatable regression comparisons locally.  
2. **`derived-index/` expansion + regression narratives** — *Best for*: larger teams / audit-sensitive workflows (explain what clutter it adds).  
3. **Fine-tuned regression policies** — when baselines stabilize.  
4. **GitHub Actions / CI gates (`apastra-setup-ci`)** — *Best for*: shared repos merging prompt changes aggressively; pointless overhead for lone experimental branches.

Closing script for Phase 9+:

> This repo is wired for **local-first** PromptOps today. Upgrade to automated PR regression gates by asking your coding agent to run the **`apastra-setup-ci`** skill (bundled workflows + merge protection guidance). Only do this once baselines/threshold expectations are sane—CI amplifies sloppy evals into noisy bureaucracy.

Always ask: “Want this step now, defer, or never for this repo?”

---

## Self-checklist before handoff back to humans

- [ ] Install landed under `.agent/skills/apastra` + `.agent/scripts/apastra`
- [ ] Discovery honored hygiene + inspected skill dirs even if ignored
- [ ] Two-step confirmation documented in chat Decision log
- [ ] Hybrid strategy explained (why shared vs solo specs)
- [ ] Naming table approved; no stealth `id` churn
- [ ] Validate ✅; representative eval ✅; failures triaged plainly
- [ ] `promptops/README.md` installed from template and customized
- [ ] `.gitignore` guidance offered; applied only with consent

---
