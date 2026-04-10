# Reference Adapter

Apastra operates on a "bring your own harness" model. This reference adapter is a minimal mock implementation designed to show the shape of the execution trace that Apastra evaluates.

## Using Claude Code as a Harness

Claude Code is an excellent choice for a default, production-grade harness, especially for evaluating skills and workflows.

To use Claude Code (or other environments like Vercel AI SDK, OpenAI Responses API, etc.) as your harness:
1. Run your evaluations using Claude Code.
2. Have your harness wrapper capture the prompt, inputs, events, and results.
3. Export the trace into the Apastra standard run artifact format (`run_manifest.json`, `scorecard.json`, etc.).
4. Use Apastra to standardize the evaluation of these runs.

Apastra standardizes the *evaluation* of the runs, not the execution itself. Keep your runtime, export the run!
