---
name: apastra-setup-ci
description: Upgrade from local-first evaluation to automated GitHub Actions CI. Installs workflows for PR gating, release promotion, and auto-merge.
---

# Apastra CI Setup

Upgrade your local-first PromptOps workflow with GitHub Actions. This adds PR gating, release automation, and autonomous promotion tracking to your repository.

Apastra is designed to be **CI optional**. You can start local-first (using your IDE agent as the harness) and upgrade to CI any time just by dropping these workflows into your repository. The core file-based protocol never changes.

## When to Use

Use this skill when you want to:
- Enforce that pull requests pass prompt evaluations before merging
- Block PRs that cause prompt regressions against known baselines
- Automate immutable releases of approved prompt packages
- Track promotions of prompts to production environments

## How to Set Up CI

When the user asks to "set up apastra CI" or "upgrade to CI", do the following:

### Step 1: Copy Workflow Templates

This skill includes pre-built GitHub Actions workflows in its `templates/.github/workflows/` directory.

Copy these directly into the user's project:

```bash
mkdir -p .github/workflows
cp -r .agents/skills/apastra-setup-ci/templates/.github/workflows/* .github/workflows/
```

### Step 2: The 5 Workflows Installed

Explain what these workflows do for the project:

1. **`regression-gate.yml`**
   - **Trigger**: Pull requests
   - **Action**: Runs the "regression" suite (a designated heavy suite) against the prompt changes. Compares results to the stored baseline.
   - **Effect**: Blocks merge if a regression is detected beyond allowed policy thresholds.

2. **`auto-merge.yml`**
   - **Trigger**: CI pass
   - **Action**: If all required checks pass (including `regression-gate`), it automatically merges the PR.

3. **`promote.yml`**
   - **Trigger**: Manual dispatch or successful release
   - **Action**: Creates an append-friendly promotion record in `derived-index/promotions/` linking the verified digest to the `prod` channel.

4. **`deliver.yml`**
   - **Trigger**: After promotion
   - **Action**: Syncs approved and promoted prompt versions to downstream delivery targets (e.g., config stores or edge endpoints).

5. **`immutable-release.yml`**
   - **Trigger**: Pushing a tag (e.g., `v1.2.0`)
   - **Action**: Creates an immutable GitHub Release, ensuring the assets cannot be tampered with after publication.

### Step 3: Configure Required Status Checks

Advise the user to go to their GitHub repository settings:
1. Navigate to **Settings** > **Branches**
2. Add a branch protection rule for their main branch
3. Enable **Require status checks to pass before merging**
4. Add the `promptops-regression-gate` job to the required list.

Now no one (not even an autonomous agent) can merge a prompt change that drops quality below the established baseline.

## Next Steps

Remind the user that the core workflow remains the same:
- They still edit prompts in `promptops/prompts/`
- They still write cases in `promptops/datasets/`
- They still test locally using `npx skills add BintzGavin/apastra/skills/eval`
- The only difference: when they push a PR, GitHub Double-Checks the results.

## Agent Context

You (the agent editing the user's code) do not need to rewrite or configure complex cloud integrations. The GitHub Actions workflows handle the external compute. Just ensure the files exist in `.github/workflows/`.
