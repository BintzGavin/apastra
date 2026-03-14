# Naming Policy

This document outlines the rules for naming packages, prompts, metrics, and handling renames.

## Stable Prompt IDs
- Every prompt must define a stable `id` in its spec.
- The `id` should be lowercase alphanumeric with hyphens (e.g., `my-app/summarize-v1`).
- The `id` is the primary identifier for consumption, overrides, and telemetry.

## Package Naming
- Packages published to the registry must have unique, descriptive names.
- Namespaces should map to organizational boundaries (e.g., `@acme/customer-support`).

## Rename Policy
- Prompts and packages should generally not be renamed.
- If a rename is necessary, a new prompt/package should be created, and the old one should be deprecated using the deprecation policy.
- Hard aliasing is not supported at the registry level to prevent ambiguity and cache invalidation complexity.

## Metric Naming
- Metrics defined in evaluators and scorecards must have clear, stable names.
- To prevent silent semantic drift, if a metric's logic changes significantly, its version should be incremented or a new metric name should be introduced (e.g., `exact_match_v2`).
