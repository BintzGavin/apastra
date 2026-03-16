# Federation Policy

This document outlines the governance rules for cross-custodian trust and namespace resolution within the Black Hole PromptOps ecosystem.

## Namespace Resolution

To ensure prompts can be uniquely identified and discovered across different custodians, all federated prompt IDs must be fully qualified.

*   **Format:** `@<custodian>/<prompt-id>`
*   **Example:** `@apastra/customer-support-agent`

Local overrides and git references within a single custodian's domain may omit the custodian prefix, defaulting to the local namespace.

## Cross-Custodian Trust

Federation enables multiple independent registries (custodians) to interoperate.

1.  **Trust Establishment:** Trust between custodians is explicitly defined via approved delivery targets and verification of provenance attestations.
2.  **Responsibility:** Each custodian is independently responsible for enforcing their own Acceptable Use and Moderation policies (`acceptable-use.md`, `takedowns.md`, `appeals.md`).
3.  **Sync by Digest:** When referencing prompts across custodian boundaries, the reference must always use the content digest to guarantee immutability and verifiable resolution.

## Shared Protocol

Federated custodians agree to support the standard consumption manifest format and the core artifact resolution protocols to allow prompt discovery, execution, and metric comparability across boundaries.
