# Answer: did this change make my assistant worse?

The provider owns execution, one explicitly selected workspace, its trusted adapter,
and retained evidence. Kody composes remote operations in a user-owned package.
No service, account, model purchase, baseline promotion, or release is implicit.

## Acceptance criteria

- Given a workspace and owner-selected adapter, when a candidate starts, then the
  provider returns a durable run ID promptly, reports queued/running/completed or
  interrupted status, and retains the exact input snapshot and measured evidence.
- Given no adapter or a historical revision, when execution is requested, then it
  returns unsupported and never claims evaluation completion or checks out code.
- Given a malformed suite or unsafe workspace, asset, adapter, or output path,
  when requested, then it fails before execution or reading unrelated files.
- Given complete baseline and candidate evidence, when compared, then the existing
  admission and regression runtime checks case/config/metric comparability and
  returns metric differences and inspectable changed-case references.
- Given changed cases, evaluator/config, missing evidence, a failing baseline, or
  no evaluation policy, when compared, then the answer is inconclusive, never an
  invented regression. A candidate threshold failure is distinct from regression.
- Given a local deterministic uppercase assistant, when its prompt changes to
  lowercase, then the same cases regress; restoring uppercase verifies the fix.
  This measures a local program, not a paid model or statistical significance.
- Given a slow, broken, timed-out, or interrupted adapter, when status is read,
  then progress/failure is useful, bounded, and contains no adapter stdout/stderr.
- Given HTTP transport, when no valid owner JWT with the configured audience,
  issuer, subject and scope is provided, then access fails. Host/Origin and MCP
  protocol protections remain enabled. Stdio remains available to local hosts.
- Given the supported CLI launcher, when a real MCP client initializes, lists,
  starts, polls, compares and inspects, then structured results survive the wire.
- Given the reusable Kody package, when its start/resume exports run, then they
  select the expected workspace/suite, preserve explicit baseline identity,
  surface pending/failed/unsupported states and concise evidence-backed differences.

## Boundaries

One server per owner/workspace; the authenticated subject is fixed by the owner.
The launcher binds loopback HTTP behind an owner-operated HTTPS reverse proxy.
Public-key JWT validation never requires the provider to hold signing secrets.
Local files and adapter executables are owner-trusted; content digests are integrity
checks, not signatures. No claim about live OAuth, hosted Kody execution, paid
models, or statistical confidence follows from deterministic local acceptance.
