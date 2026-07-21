# Provider request logging

Status: implementation contract

## Product promise

Apastra can opt a user into seeing the complete request bodies their coding-agent
harness sends to Anthropic or OpenAI. The feature is local-first, disabled until
the user explicitly enables it, and usable either for one launched session or as
a reversible persistent routing configuration.

The logger makes the model boundary inspectable: system/developer instructions,
conversation history, tool definitions, tool results, model settings, and any
other JSON fields present in the provider request are preserved byte-for-byte.
Authentication headers are forwarded in memory but are never written to disk.

## Supported integrations

The adapter picker supports:

- Codex
- Claude Code
- OpenCode
- Pi
- generic OpenAI-compatible clients
- generic Anthropic-compatible clients

Codex, OpenCode, Pi, and generic clients may route OpenAI-format requests.
Claude Code, OpenCode, Pi, and generic clients may route Anthropic-format
requests. A selected adapter can enable either or both protocols when the agent
supports both.

## Explicit non-goals

- Capturing traffic without the user's knowledge
- TLS interception or installing a local certificate authority
- Recording authentication, cookie, or proxy-authorization headers
- Sending request logs to Apastra or another hosted service
- Claiming that provider-side transformations after receipt are visible
- Treating lifecycle/tool hooks as equivalent to provider request capture

## Configuration contract

Configuration is versioned JSON in a user-scoped Apastra config directory. Tests
and automation can override that directory with `APASTRA_CONFIG_DIR`.

The request-logging configuration records:

- enabled/disabled state
- selected adapters and protocols
- an absolute user-selected save directory
- activation mode (`session` or `persistent`)
- retention in days (default `7`)
- maximum retained bytes (default `262144000`, 250 MB)
- loopback host and port
- explicit OpenAI and Anthropic upstream origins

The gateway binds only to a loopback address. A non-loopback host is rejected.
Upstreams default to the official provider origins. A custom upstream is allowed
only through an explicit configuration choice and must be an HTTP(S) origin.

## CLI contract

The package exposes an `apastra` executable. The following command family is
stable:

```text
apastra request-log configure
apastra request-log status [--json]
apastra request-log serve
apastra request-log run <adapter> [--provider <provider>] -- [agent arguments]
apastra request-log install <adapter> [--provider <provider>] [--dry-run]
apastra request-log disable [<adapter>]
apastra request-log list
apastra request-log show <request-id>
apastra request-log prune
```

`configure` is an interactive onboarding wizard unless all required values are
provided noninteractively. It must:

1. Explain that full prompts, private code, tool schemas, and conversation history
   can be stored.
2. Require an explicit confirmation; Enter alone does not enable capture.
3. Let the user choose any supported adapter subset.
4. Let the user choose the save directory.
5. Offer session-only activation first and persistent activation second.
6. Offer the seven-day/250 MB defaults and allow either to be changed; indefinite
   retention requires an explicit choice.
7. Print the resulting configuration and exact next command.

`status` reports whether capture is enabled, selected adapters, save directory,
retention, gateway status, and installed persistent routes. `disable` is
idempotent. Disabling one adapter leaves the others active. Disabling the final
adapter stops persistent routing and capture.

## Session-only activation

Session-only mode does not edit persistent agent configuration.

- Codex is launched with a temporary OpenAI base-URL override.
- Claude Code is launched with a process-local `ANTHROPIC_BASE_URL`.
- OpenCode is launched with a merged process-local `OPENCODE_CONFIG_CONTENT`.
- Pi is launched with an isolated `PI_CODING_AGENT_DIR` that preserves the user's
  existing resources and credentials while overriding provider base URLs only.
- Generic integrations print/export provider-specific base URLs and can launch a
  supplied command with those values in its environment.

The gateway lifecycle follows the launched child process. Interrupt and exit
codes are propagated. Temporary adapter configuration is removed after exit.

## Persistent activation

Persistent activation is a separate, explicit action. Before changing a config
file, Apastra prints the target and proposed change. It stores a private backup
and an install-state record containing the before/applied digests.

Disable restores the original only when the current file still matches the
Apastra-applied digest. If the user or another tool edited the file afterward,
Apastra refuses to overwrite it and explains how to resolve the conflict.

Persistent routing is supported for every named adapter. It uses each agent's
documented user-level provider/base-URL configuration. Apastra-owned keys are
namespaced where the format permits it and unrelated settings are preserved.

## Gateway routing contract

The gateway exposes adapter-specific provider bases:

```text
http://127.0.0.1:<port>/openai/<adapter>/v1
http://127.0.0.1:<port>/anthropic/<adapter>
```

The remainder of the request path and query is forwarded to the configured
provider origin. Only configured provider/adapter combinations are accepted.
Unknown routes return a local error and are never forwarded.

The gateway:

- preserves the exact request body bytes sent by the client
- forwards request method, query, body, and required provider headers
- removes hop-by-hop headers
- never records request headers or query values
- streams the upstream response without storing its body
- records response status, duration, and upstream failure class as metadata
- returns a local error without forwarding if the request body cannot be durably
  written (fail closed)
- applies retention only to directories carrying an Apastra log marker

## Log artifact contract

Each request has its own directory:

```text
<save-dir>/<YYYY-MM-DD>/<timestamp>_<request-id>/
  .apastra-request-log
  request.body
  metadata.json
```

`request.body` contains the exact bytes received from the client. `metadata.json`
contains schema version, request ID, timestamp, provider, adapter, method, path
without query values, content type, byte length, SHA-256 digest, response status,
duration, and error classification. It contains no request headers or response
body.

Directories are mode `0700` and files are mode `0600` on platforms that support
POSIX permissions. If the chosen directory is inside a Git worktree, Apastra adds
the exact path to `.git/info/exclude`; it does not modify the tracked `.gitignore`.
The worktree root is rejected as a save directory because it cannot be excluded
as one exact path; the user must choose a dedicated subdirectory.

`list` shows request ID, time, provider, adapter, model (when parseable), body
bytes, and status. `show` prints metadata and a pretty JSON body when valid JSON,
falling back to a byte-safe representation for other content.

## Retention contract

Retention runs at gateway startup, after a completed request, and through
`prune`. It enforces both age and total-size limits, oldest first. It never
deletes an unmarked directory or any file above the configured save directory.
`0` days means indefinite age retention only after explicit user confirmation;
`0` maximum bytes means no size cap only after explicit confirmation.

## Behavioral acceptance criteria

### AC-01: disabled by default

Given Apastra is freshly installed, when any request-log status or setup command
runs, then no agent configuration is changed, no gateway starts, and capture is
reported disabled.

### AC-02: explicit onboarding opt-in

Given the onboarding wizard, when the user accepts defaults without answering the
capture confirmation affirmatively, then request logging remains disabled.

Given the user explicitly opts in, selects adapters, and chooses a save directory,
when onboarding completes, then the versioned configuration contains those exact
choices and prints a usable session command.

### AC-03: exact OpenAI request capture

Given a fake OpenAI upstream and a configured Codex route, when a client sends a
request containing system/developer input, conversation items, tools, and model
settings, then the upstream and `request.body` receive identical bytes and the
log identifies provider `openai` and adapter `codex`.

### AC-04: exact Anthropic request capture

Given a fake Anthropic upstream and a configured Claude Code route, when a client
sends a Messages request containing system content, messages, tools, and model
settings, then the upstream and `request.body` receive identical bytes and the
log identifies provider `anthropic` and adapter `claude-code`.

### AC-05: credentials are never persisted

Given requests with `Authorization`, `x-api-key`, cookies, and proxy credentials,
when capture completes or forwarding fails, then none of those values occur in
any file under the save directory or Apastra config directory.

### AC-06: every adapter has a faithful launch route

Given each supported adapter, when Apastra builds a session launch, then only the
child-process environment/arguments/config directory are changed and both the
provider and adapter appear in its gateway base URL.

### AC-07: persistent changes are reversible and conflict-safe

Given a persistent install, when disable runs without intervening edits, then the
original config bytes are restored. Given an intervening edit, disable refuses to
overwrite it and preserves both the current file and backup.

### AC-08: save location and permissions

Given a user-selected save directory, when a request is captured, then all log
artifacts appear only under that directory with private permissions and an
in-repository location is excluded through `.git/info/exclude`.

### AC-09: retention is bounded and scoped

Given marked and unmarked old directories, when retention runs, then expired or
over-cap marked logs are removed oldest-first and unmarked content is untouched.

### AC-10: forwarding is transparent

Given success, provider error, streaming response, timeout, and client disconnect
cases, when traffic passes through the gateway, then status, relevant response
headers, body chunks, and failure semantics reach the client without response
body persistence.

### AC-11: logging failure is visible

Given an unwritable or full save destination, when a request arrives, then the
gateway does not forward it and returns a local logging error.

### AC-12: packaged and documented

Given an npm package tarball or Git-clone installation, when Apastra is installed,
then the CLI, request-log runtime, onboarding instructions, and this contract are
present and the documented smoke command succeeds without provider credentials.

## Required quality evidence

Completion requires:

- unit tests for configuration, route parsing, retention, permissions, and config
  mutation/restore
- adapter launch-contract tests for Codex, Claude Code, OpenCode, Pi, and generic
  clients
- local integration tests against fake OpenAI and Anthropic streaming upstreams
- end-to-end CLI tests for configure/status/run/install/disable/list/show/prune
- mutation testing of credential non-persistence, route validation, fail-closed
  logging, and retention boundaries
- Python syntax checks, schema validation, package-content verification, and an
  installed-package smoke test
