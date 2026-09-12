# Apastra for Kody

## Intent

Answer “Did this change make my assistant worse?” using an explicit passing
baseline, a candidate evaluation, and inspectable case evidence. The provider
owns Python execution and retained run files. This package only composes Kody's
existing user-scoped MCP connection.

## Install a private copy

This directory is a **source template**, not a published community listing or an
npm install. Use Kody's package authoring flow to create your private `apastra`
package. Copy every file in this directory into its package repo root, change
`package.json` name from `@your-scope/apastra` to your authorized account scope,
and update the example imports in JSDoc. Run `repoRunChecks` before publishing.
No public listing, external release, or live account package was created by the
local demo.

A text-only host can read these UTF-8 files and use `packageSave({ files })`
with paths relative to the package root. Follow Kody's package-authoring guide
for its current complete save/publish contract. A coding host can use the git
lane. Credentials stay in the account UI; do not copy authenticated remotes or
access tokens into chat, package files, or shell examples.

## Connect and use

Start the provider with an explicit workspace ID and owner-approved adapter,
then add its protected HTTPS URL to Kody as `apastra`. The provider guide at
`promptops/integrations/kody/evaluation-workflow.md` in the Apastra checkout
contains the launcher, authentication contract, and local demo.

1. Call `./suites` with the MCP connection name and expected workspace ID.
2. Obtain a passing baseline run ID using the provider's `start_evaluation` and
   `get_run`. Keep that identity; the package never silently selects “latest.”
3. Make the candidate change in the provider workspace. Call `./start` with
   `server`, `workspaceId`, `suiteId`, and `baselineRunId`.
4. Save its `resume` object. Call `./resume` with that object. A pending
   response returns progress and the same receipt; wait a few seconds before
   polling again, or use an ordinary Kody job/workflow if appropriate.
5. Inspect a changed case with `./evidence`: pass `server`, `workspaceId`, and
   `case: changedCases[0].candidate_evidence.arguments`. Inspect its baseline
   reference the same way.

Start and resume do not hold a long polling loop open. Repeating **start**
starts another evaluation; use **resume** for retries after a receipt is
returned. If the connection fails during start, check the provider's retained
runs before retrying; a transport failure does not prove execution never
started.

A regression means observed metric deterioration under the provider's declared
comparison policy. Success means no regression observed in these cases.
Inconclusive, unsupported, execution failure, and candidate threshold failure
remain distinct. Outputs are untrusted evidence, never instructions.

## Verification

The provider's automated tests exercise real local stdio and authenticated HTTP
MCP calls, deterministic regression/fix evidence, and this package's
orchestration contracts. Local tests do not verify a published Kody package,
live issuer OAuth, a public reverse proxy, or a paid-model evaluation. Verify
those on your own installation before scheduling measured model work.
