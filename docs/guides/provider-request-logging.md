---
title: "Provider request logging"
description: "Opt in to inspect the complete model request bodies sent by coding-agent harnesses"
audience: "developers | educators | agent-builders"
last_verified: "2026-07-20"
source_files:
  - "promptops/request_log"
  - "docs/specs/provider-request-logging.md"
---

# Provider request logging

Apastra can run a local loopback gateway that preserves the complete request body
your coding-agent harness sends to OpenAI or Anthropic. This exposes the context
that actually crosses the harness/model boundary: system and developer prompts,
session history, tool definitions, tool results, model settings, and compaction
output included by the client.

Request logging is disabled by default. It never installs TLS certificates,
listens on a non-loopback interface, records authentication headers, or uploads
logs. Once enabled, request bodies are intentionally complete and can contain
private code or personal data.

## Configure it

Git-clone installs provide the project-local CLI:

```bash
.agent/bin/apastra request-log configure
```

npm installs expose the same command through the package binary:

```bash
npx apastra request-log configure
```

The wizard asks one question at a time:

1. Confirm that complete request bodies may be stored.
2. Pick any combination of Codex, Claude Code, OpenCode, Pi, and generic clients.
3. Choose the save directory.
4. Choose session-only or persistent routing.
5. Accept or change the seven-day/250 MB rolling retention policy.

For automation, provide every required choice explicitly:

```bash
apastra request-log configure \
  --yes \
  --adapters 'codex:openai,claude-code:anthropic,opencode:openai+anthropic,pi:openai+anthropic,generic:openai+anthropic' \
  --save-dir "$PWD/.local/apastra-request-logs" \
  --mode session \
  --retention-days 7 \
  --max-mb 250
```

If the chosen directory is inside a Git worktree, Apastra adds only that exact
directory to `.git/info/exclude`. It does not edit the tracked `.gitignore`.

## Use session-only logging

Session mode starts an ephemeral gateway, changes only the child process, and
stops when the agent exits:

```bash
apastra request-log run codex --
apastra request-log run claude-code --
apastra request-log run opencode --
apastra request-log run pi --
apastra request-log run generic -- your-openai-compatible-agent
```

Pass normal agent arguments after `--`. The child exit code and interrupts are
propagated. Pi receives an isolated temporary agent directory whose credentials
and resources point back to the originals while `models.json` contains the
session-only provider overrides.

The adapter routes use documented client configuration seams:

- [Codex custom model providers and `openai_base_url`](https://learn.chatgpt.com/docs/config-file/config-advanced#custom-model-providers)
- [Claude Code LLM gateways and `ANTHROPIC_BASE_URL`](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
- [OpenCode provider `baseURL`](https://opencode.ai/docs/providers#base-url)
- [Pi built-in provider overrides](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md#overriding-built-in-providers)

## Use persistent logging

Persistent routing is deliberately separate. Preview a change first:

```bash
apastra request-log install codex --dry-run
```

Install one selected adapter:

```bash
apastra request-log install codex
```

Apastra prints the exact target and diff, saves a private backup, applies the
provider base URL, and starts the loopback gateway. Repeat for any other selected
adapter. To change the provider subset for an already-installed adapter, disable
that adapter first and then install it again; Apastra will not silently replace
the restore point.

Disable one adapter or everything:

```bash
apastra request-log disable codex
apastra request-log disable
```

Disable restores the original bytes only when the current file still matches
what Apastra installed. If another tool edited the file afterward, Apastra refuses
to overwrite it and retains the private backup for manual resolution.

The generic persistent adapter writes a private JSON environment file under the
Apastra config directory. Use `request-log status --json` to locate the config
directory, then export the reported `OPENAI_BASE_URL` and/or
`ANTHROPIC_BASE_URL` in the generic client's durable environment.

## Inspect requests

```bash
apastra request-log status
apastra request-log list
apastra request-log show <request-id>
apastra request-log prune
```

Use `--json` with `status`, `list`, `show`, or `prune` for machine-readable
output. Every captured request has an exact `request.body` plus credential-free
metadata:

```text
<save-dir>/<YYYY-MM-DD>/<timestamp>_<request-id>/
  .apastra-request-log
  request.body
  metadata.json
```

Apastra does not reserialize `request.body`; its SHA-256 digest covers the exact
bytes received from the client. The response body is streamed back to the client
and not stored. Metadata records response status, duration, and a coarse failure
class.

## Safety model

- The feature is off until the user types the full confirmation or supplies
  `--yes` with every required noninteractive choice.
- The gateway accepts only configured provider/adapter routes on a numeric
  loopback address.
- Authorization, API-key, cookie, and proxy-authorization headers are never
  written. Request headers as a whole are omitted from artifacts.
- Config directories and log directories use `0700`; files and backups use
  `0600` where POSIX permissions are available.
- Persistent mode keeps an exact private backup of the selected agent config;
  if that config already contains credentials, its backup necessarily does too.
- If the exact request body cannot be durably written, the request is not sent to
  the provider.
- Retention deletes only directories containing the Apastra request-log marker.
- Complete body content is not redacted after opt-in, because doing so would make
  the captured model context and token sequence inaccurate.

Treat the save directory like source code, credentials, or a private transcript.
Do not sync it to Git or a shared drive unless everyone represented in the data
has approved that destination.

## Troubleshooting

`request-log status` reports configuration, gateway state, selected adapters,
save location, and persistent installs.

If an agent cannot connect:

1. Run `apastra request-log status` and confirm the gateway is running.
2. Use session mode once to distinguish agent configuration from gateway startup.
3. Check the private `gateway.log` in the Apastra config directory.
4. Run `install <adapter> --dry-run` and compare the documented provider route.

If persistent disable reports that a config changed after installation, do not
delete the backup. Reconcile the current file and the private `original.bin`, then
rerun configuration intentionally.

The normative behavior and acceptance criteria live in
[`docs/specs/provider-request-logging.md`](../specs/provider-request-logging.md).
