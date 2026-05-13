---
name: apastra-trace
description: Inspect agent traces, hook events, tool-call transcripts, and run artifacts; turn them into PromptOps evidence, eval cases, and artifact references.
---

# Apastra Trace

Use this skill when the user wants to understand what an agent did, debug a failed agent workflow, convert tool-call traces into eval coverage, or attach trace evidence to a PromptOps run.

## Core Idea

Agent traces are evidence. They show not only the final answer, but the path: prompts, tool calls, arguments, retries, refusals, validation failures, edits, and stopping conditions. Apastra uses hooks to expose that path during local work, then stores durable evidence as run artifacts or artifact references.

Hooks are not a blanket telemetry sink. Do not persist raw secrets, private transcripts, or full tool payloads unless the user explicitly asks and the destination is appropriate. Prefer sanitized summaries, stable artifact references, and content digests.

## When to Use

Use `apastra-trace` when:

- A model output passed, but the agent used the wrong steps or tools
- A coding agent made an unsafe edit, skipped validation, or stopped too early
- A trace/log/transcript contains a real failure that should become a regression case
- The user asks what evidence should be attached to `artifact_refs.json`
- Hooks surfaced a validation or safety issue and the user wants it turned into coverage

## Workflow

1. **Locate trace sources**

   Check available sources in this order:
   - Current agent transcript or tool history
   - Apastra hook feedback from Codex or Claude Code
   - `promptops/runs/<run-id>/cases.jsonl`
   - `promptops/runs/<run-id>/artifact_refs.json`
   - External observability exports, logs, or saved traces supplied by the user

2. **Sanitize before storing**

   Remove API keys, private tokens, PII, irrelevant raw prompts, and large payloads. If raw material must be retained, store it outside Git and record only URI, digest, media type, and retention notes in `artifact_refs.json`.

3. **Extract behavioral evidence**

   Identify the observable behavior:
   - Required or forbidden tool calls
   - Tool arguments and file paths
   - Retry behavior
   - Validation output
   - Stop/continue decisions
   - Duration, token/cost metadata, or timeout
   - Final output and intermediate artifacts

4. **Choose the eval surface**

   Classify the case as:
   - **Outcome**: final answer/content is right or wrong
   - **Step**: agent followed or skipped required process
   - **Trace**: tool sequence, arguments, or stopping condition is the thing being tested

5. **Create or update eval coverage**

   For new coverage, pair with `apastra-writing-evals` to design the measurement, then use `apastra-scaffold` to create the prompt spec, dataset, evaluator, suite, or quick eval. Prefer deterministic trace checks when tool names, file paths, arguments, or validation messages are observable.

6. **Attach artifact references**

   When evidence is too large or sensitive for Git, add references instead of raw payloads:

   ```json
   {
     "artifact_id": "agent-trace-2026-05-13-001",
     "kind": "agent_trace",
     "uri": "s3://example-bucket/path/to/redacted-trace.jsonl",
     "digest": "sha256:<digest>",
     "media_type": "application/jsonl",
     "notes": "Redacted Codex/Claude hook trace for failed validation run."
   }
   ```

7. **Validate and run**

   Run `apastra-validate`, then `apastra-eval`. Read failed traces before changing thresholds; trace failures usually mean the behavior definition is underspecified or the agent skipped a required step.

## Output Expectations

When reporting back, include:

- What trace source was inspected
- What evidence was extracted
- What was redacted or intentionally not stored
- Which eval cases or artifact refs were created or updated
- What validation/eval commands were run
