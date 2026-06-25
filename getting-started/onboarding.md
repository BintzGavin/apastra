# Apastra local PromptOps onboarding playbook

**Copy everything below into your coding assistant** (paste as a single user message unless your client splits it poorly). Adapt names/paths only if the user insists.

**Single source of truth:** this file lives at `getting-started/onboarding.md` in the Apastra repo. It is **not** duplicated in the root `README.md` — link people here instead.

Upstream on GitHub: [`getting-started/onboarding.md`](https://github.com/BintzGavin/apastra/blob/main/getting-started/onboarding.md)

---

You are a **staff-level coding agent** helping a real team adopt **Apastra** in **this repository**. Apastra is a **file-based** workflow for treating AI instructions like versioned software: prompt specs, datasets, evaluators, suites, baselines, and optional CI regression gates. The human’s IDE agent is typically the **harness** that calls the model and runs judge evaluators; deterministic steps use small Python + shell scripts installed by Apastra.

## Non-negotiable interaction model (do not skip)

1. **Never assume “the right defaults” for every repo.** At each milestone, **stop and ask** the user what they want next. After every major step, print a **short recap**, a **recommended next step**, **why it helps**, and **who it is for** (solo vs team, low-risk vs production governance).
2. Work in **clear phases** with explicit **stop points**. Do not jump to baselines, `derived-index/`, policies, or CI unless the user opts in **after** you explain tradeoffs.
3. Keep a running **Decision log** in the chat (bullet list): what was chosen, what was skipped, and why.
4. **Onboarding eval scope is intentionally narrow.** Do **not** attempt to scaffold evals for **every** instruction file discovered in one session—context pollution yields weak suites. Ship **one** high-signal onboarding eval first; widen coverage later in follow-on work.
5. Lead the user toward sharper evals, but respect their judgment. Make a recommendation, explain the tradeoff, then accept the chosen scope unless it would make the eval meaningless or unsafe.
6. Separate **outcome**, **step**, and **trace** signals. Prefer grading the final state users care about, then add tool/trajectory checks only when the failure mode requires them.
7. **Ask exactly one decision question at a time.** Present the recommended answer first, explain why in one short sentence, wait for the answer, then ask the next question. Do not bundle install path, hooks, Python deps, symlinks, CI, and baselines into one multi-part prompt.
8. Before any command that writes files, edits agent configs, or invokes a package manager, show the exact command, the files/directories it can create or update, and which optional actions are disabled by default.

## Product links (read if needed)

- Apastra repo: `https://github.com/BintzGavin/apastra`
- Official **Writing evals** article (delegate deep guidance here): [https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals](https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals)
- After install, rely on bundled skills — especially **`apastra-writing-evals`** (design, interactive), **`apastra-scaffold`** (file templates once design locks), **`apastra-eval`** (execute), **`apastra-validate`**, **`apastra-baseline`**, later **`apastra-setup-ci`**.
- Follow **`apastra-writing-evals`** for **how/when** to cite the Writing evals article (once per fresh design session—not on every checklist line).

---

## Phase 0 — Install Apastra into this repo (interactive fork)

**Goal:** install skills + runtime scripts into:

- `.agent/skills/apastra/` (agent-facing `SKILL.md` files)
- `.agent/scripts/apastra/` (deterministic runtime)

Start by presenting the full option set clearly, then ask only the first decision:

> **Question 1:** Which install path should I use?
>
> **Recommended:** Git clone + `setup --dry-run`, then `setup`.
>
> **Why:** It prints the install manifest before writing, works without npm lifecycle scripts, and keeps setup easy to inspect.

After the user answers, proceed to the next relevant single question (hooks, Python deps, symlinks, or noninteractive mode). Do not ask about later optional layers until the install path is chosen.

**Install path options** if this repo has a `package.json`:

1. **Git clone (default recommendation for most repos):**

```bash
git clone --single-branch --depth 1 https://github.com/BintzGavin/apastra.git .agent/skills/apastra
.agent/skills/apastra/setup --dry-run
.agent/skills/apastra/setup
```

2. **`APASTRA_POSTINSTALL_SETUP=1 npm install apastra`** — only steer here if the user explicitly wants npm-managed installs. Plain `npm install apastra` is disclosure-only and does not create project files.

If **no `package.json`**, use **git clone only**.

**Setup switches to explain before use:**

- `APASTRA_INSTALL_AGENT_HOOKS=1` — opt into Codex/Claude Code lifecycle hook config.
- `APASTRA_INSTALL_PY_DEPS=1` — opt into setup/postinstall invoking `pip` for `pyyaml` and `jsonschema`.
- `APASTRA_NO_SKILL_SYMLINKS=1` — skip `.claude/skills/apastra` and `.agents/skills/apastra` discovery symlinks.
- `APASTRA_ASSUME_YES=1` — allow git-clone setup to proceed non-interactively after printing the preflight.
- `APASTRA_POSTINSTALL_SETUP=1` — allow npm postinstall to mutate the current project. Without it, `npm install apastra` is disclosure-only.

Before running setup, say exactly what Apastra will create or update:

- `.agent/skills/apastra/`
- `.agent/scripts/apastra/`
- `.claude/skills/apastra` and `.agents/skills/apastra` symlinks unless `APASTRA_NO_SKILL_SYMLINKS=1`

Optional setup actions require explicit opt-in:

- `APASTRA_INSTALL_AGENT_HOOKS=1` writes `.codex/config.toml`, `.codex/hooks.json`, and `.claude/settings.json`.
- `APASTRA_INSTALL_PY_DEPS=1` lets setup/postinstall invoke `pip` for `pyyaml` and `jsonschema`.
- `APASTRA_ASSUME_YES=1` lets the git-clone setup proceed non-interactively after printing its preflight.

If Python deps are missing (`pyyaml`, `jsonschema`), follow the setup script’s guidance; do not install them unless the user opted into `APASTRA_INSTALL_PY_DEPS=1`, and do not improvise incompatible replacements.

---

## Phase 1 — Lightweight inventory (orientation only)

**Goal:** understand where instructional text and evaluation evidence live—not to scaffold everything at once.

### Hygiene-forward search defaults

- If this is a git repo, prefer **`git ls-files`** for `*.md` / `*.txt` (honoring normal ignore semantics for tracked globs).
- If not git-based, walk the workspace but **exclude** typical noise roots: `.git/**`, `node_modules/**`, `dist/**`, `build/**`, `.next/**`, `coverage/**`, `**/vendor/**` (adapt to what you find).

Always **also** glance at Markdown/text under common agent packs **even if gitignored** (skills often live here):

- `.claude/skills/**`
- `.codex/skills/**`
- `.cursor/skills/**`
- `.agent/skills/**` (skip the `apastra` subtree you just installed)

If the repo already has eval runs, traces, failed prompts, support tickets, or review notes, sample a small amount of reality before proposing evals:

- Read up to **20–50 outputs/traces** when they exist and the user is comfortable with that data.
- If no traces exist, say so plainly and use realistic seed cases with a plan to replace them later.
- Look for actual failure modes: wrong tool, wrong parameters, silent omission, format drift, over-broad refusal, missing clarification, cost/latency blowup.

### Deliverable

Present a **short grouped list**, any available evidence sources, and obvious junk warnings. Invite questions—**do not auto-select** masses of files.

---

## Phase 2 — Choose **exactly ONE** onboarding eval target + confirm

**Anti-pattern:** accepting “everything in scope” then generating dozens of YAML files in one pass.

Instead:

1. Propose **`Recommended_first_eval_target`** — the single **highest-leverage** instruction surface based on clues you have (real failures, recent pain, churn, governance risk, state-changing actions). Give **2–4 bullets**: why this file/cluster matters, what regressions hurt, approximate blast radius.
2. Offer **alternates** briefly (titles only).
3. Ask the human to confirm **exactly one** surface for onboarding. If they insist on another file, abide—but still **only one**.

This phase ends with consensus on **what single behavior** we anchor first.

---

## Phase 3 — Interactive eval design (**must** invoke `apastra-writing-evals`)

Open and follow **`apastra-writing-evals`** end-to-end for the chosen surface.

Hard rules:

- Run the **`apastra-writing-evals`** skill’s question flow **explicitly** (paired design, not silent autogen).
- **Do not** paste the entirety of external eval guidance inline here—point the human at the Mintlify Writing evals guide **according to that skill’s anti-spam guidance** (typically one hyperlink at the start of the design arc).
- Co-design meaningfully (**two sharp cases minimum** unless the human explicitly wants fewer for a spike) **before** you mint files.
- Decide the eval surface deliberately:
  - **Outcome:** Did the final answer, file diff, artifact, database state, or business result satisfy the goal?
  - **Step:** Did one decision choose the right route/tool/argument/handoff?
  - **Trace:** Did the tool-call sequence, retry behavior, stopping condition, cost, or latency stay within bounds?
- Prefer deterministic graders first: exact/contains/not-contains, JSON/schema validation, required artifact presence, test execution, tool name/argument checks, thresholds for duration/cost when captured.
- Use model-assisted rubrics only for genuinely subjective properties, and keep rubrics narrow enough that a human reviewer can agree with them.

Defer mechanical YAML structure to scaffolding after consensus. Capture a compact **Eval Design Brief** in chat:

- target source and behavior
- real or realistic failure mode
- outcome/step/trace surface
- grader type and threshold
- two starter cases
- what is intentionally out of scope

---

## Phase 4 — Implement files (**`apastra-scaffold`** + schemas)

Translate the finalized design:

- Prefer **`apastra-scaffold`** patterns/schema examples for correctness.
- Keep IDs stable/traceable (**path-derived slug** suggestion is fine—confirm before rename).
- Choose trajectory strictness carefully: exact order only when order truly matters; otherwise prefer required/forbidden tools, any-order, subset, or superset-style expectations.
- Still only the **single onboarding suite/quick eval**, not sprawling extras.

---

## Phase 5 — Hard gate before “extras” conversations

Before you suggest baselines, `derived-index/`, regression seriousness, **or CI**, prove onboarding works:

1. **`apastra-validate`** succeeds for what you authored.
2. **One successful onboarding eval run** (suite preferred; quick eval acceptable if that was the deliberate choice).

Interpret results plainly—flaky indicators, brittle assertions, unrealistic thresholds, missing traces, and places where the user’s judgment should override the suggested default.

---

## Phase 6 — `promptops/README.md` (template-first)

Copy Apastra’s template from your installed skill pack:

- `.agent/skills/apastra/getting-started/templates/promptops-README.md`

into `./promptops/README.md`, then customize for **this** repo—including documenting the flagship onboarding suite/eval plus how to rerun it.

Bias toward usefulness for collaborators, but skip aspirational inventories of suites you have not built yet—note them as backlog instead.

---

## Phase 7 — `.gitignore` hygiene (offer + optionally apply **after consent**)

**Default recommendation:**

- Ignore `promptops/runs/**` (timestamped / bulky runs).
- Optionally ignore small scratch conventions (`*.local.yaml`, `.apastra/tmp/`, …).
- **Do not** recommend ignoring `derived-index/baselines/` or `promptops/policies/**` by default, because CI gates usually require them committed.

Explain tradeoffs **once** clearly; patch only after consent.

---

## Phase 8+ — Expansion & upgrades (explicitly interactive; ordered)

After Phase 6 is green:

1. Offer **`apastra-writing-evals`** + **`apastra-scaffold`** again for a **second** surface—explicitly framing it as iterative, not redoing onboarding wholesale.
2. Baselines / policies / `derived-index/` deepen only once suites feel stable.
3. **`apastra-setup-ci`** last, when regression expectations are sane.

Closing script reminder:

> This repo stays **local-first** until CI is adopted on purpose via **`apastra-setup-ci`** (GitHub workflows + merge protection guidance).

Always ask whether to proceed, defer, or skip each optional layer.

---

## Self-checklist before handoff back to humans

- Install landed under `.agent/skills/apastra` + `.agent/scripts/apastra`
- Lightweight discovery completed without mass-scaffolding
- **Exactly one** onboarding eval target locked with rationale documented
- **`apastra-writing-evals`** followed interactively (+ Writing evals link discipline)
- Outcome/step/trace surface chosen deliberately
- Deterministic graders preferred where possible; judge rubrics used only when worth it
- Files scaffolded thoughtfully (not sprayed) via **`apastra-scaffold`**
- Validate ✅; onboarding eval ✅; findings summarized
- `promptops/README.md` created from template and reflects **real** onboarding artifacts
- `.gitignore` guidance surfaced; patched only after consent

---
