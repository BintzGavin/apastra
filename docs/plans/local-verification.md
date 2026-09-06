# Local verification, September 6, 2026

Candidate checkout: `/private/tmp/apastra-trust.hQdcnc/checkout`.
Branch: `gavin/fix-evaluation-trust`.
Base: `a383e6c3b5545accabe9d938a5ae434383770680`.

Verification ran in an isolated candidate checkout. Existing research and
unrelated changes in the original checkout remain outside this worktree.
Package metadata selects version 2.0.0 for the incompatible protocol
changes. The published npm version was 1.0.1 when checked on September 6.

## Fresh verification after the scope change

On September 6, the full suite passed all 153 tests in 33.271 seconds. The first
attempt hit 13 sandbox errors when gateway tests tried to bind localhost. After
approval for local loopback access, all tests passed using synthetic child
configuration. The tests made no live-model calls.

The mutation run passed its seven-test baseline and caught all ten deliberate
faults through assertion failures. It recorded zero test setup errors and zero
survivors. `git diff --check` passed, and `git diff --quiet HEAD -- .github
setup-ci/templates` confirmed that every workflow and template remained unchanged.

After the version update, the installed-package test and both asset-inventory
tests passed in 5.289 seconds. The package test exercised the npm tarball in both
default and opt-in consumer layouts.

## Gates completed

| Gate | Evidence |
| --- | --- |
| Full local suite | 153 tests passed using the project Python interpreter and an explicit synthetic child environment. Local loopback tests required sandbox approval. |
| Installed distribution | Actual npm tarball installed offline in unrelated directories, covering default and opt-in layouts. Resolve, validate, eval, compare, gate, and request-log status passed. Documentation was present in both layouts. |
| Asset inventory | All 39 committed prompt/dataset/evaluator/suite/quick-eval files passed their correctly selected validators. Manifest-backed dataset digests were checked. Every shipped suite resolved complete inputs. |
| Targeted mutation checks | A passing seven-test baseline preceded ten mutants. All ten caused behavioral assertion failures, with zero setup errors or survivors. |
| Syntax and patch hygiene | 72 Python files parsed. Changed shell entry points passed `bash -n`, and `git diff --check` passed. |
| Independent confirmation | The cleanup task completed a bounded read-only adversarial review and confirmed the repairs listed below using additional real-process probes. |

## Reproduced failures and repairs

- Empty metrics/cases, fixture results, mismatched models or digests, incomplete
  trials, and scorecards inconsistent with cases cannot pass evaluation.
- The raw runner rejects requests that weaken suite criteria or substitute
  snapshot identities before invoking the adapter.
- Model-assisted assertions require a judge. Evaluator errors have no numeric
  score, and negation cannot convert them into passes.
- Normalization rejects missing trial scores, preserving the denominator.
- Cost and latency require measurements. Genuine zero values remain valid.
- Missing adapters and failed subprocesses cannot produce successful comparisons.
- Comparison applies cost and time budgets across the requested model set.
- Stored runs must match their content hashes and explicitly approved producer.
  Referenced local files are checked for missing or altered content.
- Regression requires typed nonempty rules and compatible metric definitions.
  A claimed flake rate cannot waive a blocking result.
- Baselines require complete passing evidence and use exclusive creation.
- CI admission checks the expected revision and current workspace digests in
  both explicit execution and evidence modes.
- Cached inline packages resolve without fetching schemas. Altered package
  content fails digest verification, and required signature verification blocks.
- Shell validators reject duplicate JSON keys and nonfinite YAML values.
- Placeholder reference execution, optimization estimates, canaries, community
  baseline generation, and observability delivery report unsupported.

The independent review reproduced the shared-cost bug: two measured 0.75 runs
passed a 1.0 suite budget through comparison. The fixed command rejects that
case, accepts equality at 1.5, and reports the measured total. Its time probe
stopped a second 0.6-second invocation under a shared one-second budget while
retaining the first run's evidence.

Additional independent probes confirmed adapter version 2.0.0 through eval,
compare, and quick eval. Missing and altered referenced files were rejected.
A real synthetic cache resolved an inline package with zero outbound schema
retrievals, then rejected changed content under the previous digest.

## Reproduce

Use an isolated test environment when host credentials are present. The full
suite's networking tests bind local loopback servers and do not call live models.

```bash
python -m unittest discover -s tests -v
python scripts/check-trust-mutations.py
python -m unittest tests.test_installed_contract tests.test_asset_inventory -v
git diff --check
```

The mutation script uses disposable copies. Its mutants cover missing adapters,
fixture results, empty coverage, evaluator errors, missing cost, manifest digest
and model mismatches, empty policies, stale revisions, and shared comparison cost.

## Scope update, September 6, 2026

The user approved keeping the runtime fixes and regression tests, dropping the
broad CI redesign, and tracking the existing false-pass gate separately. Both
repository workflows and distributed templates remain unchanged. The earlier
workflow patch was rejected and never applied.

The separate CI repair has acceptance cases in the P0 plan. Until it is verified,
the old report gate remains unsuitable for required evaluation checks. The local
runtime candidate can be reviewed independently. Its package version is 2.0.0,
and publication remains uncompleted. On September 6, `npm whoami` returned HTTP
401, so npm publication requires the owner to refresh their login locally.
Credential values were not inspected.

Live-provider behavior, judge calibration, remote delivery integrations, and
cryptographic signatures remain unverified or explicitly unsupported. These
tests establish the local execution contract, not state-of-the-art model quality.
