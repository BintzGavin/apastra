# Mirroring Policy

This document outlines the requirements and processes for establishing read-only mirrors of the official Black Hole PromptOps registry.

## Sync by Digest Protocol

To guarantee the integrity and immutability of the mirrored artifacts, all mirrors must synchronize content strictly by content-addressability (the exact cryptographic hash/digest of the prompt package).

1.  **Immutability:** A mirrored artifact, identified by its digest, must never be mutated.
2.  **Verification:** The mirror should verify the provenance and digest of every artifact synced. If a mismatch is detected, the artifact must be rejected and logged.
3.  **No Tags:** Mirrors must not rely solely on floating references (e.g., `latest` or `v1.x.x`). The canonical resolution is strictly digest-based to prevent supply chain tampering.

## Official vs. Unofficial Mirrors

### Unofficial Mirrors

*   Anyone may establish an unofficial read-only mirror of public artifacts without explicit permission.
*   Unofficial mirrors are not endorsed by the primary custodian and do not receive proactive support or notification of updates.
*   The primary registry makes no guarantees of uptime or sync latency for unofficial targets.

### Official Mirrors

*   Official mirrors represent an endorsed geographical or architectural distribution point (e.g., a sanctioned regional OCI registry).
*   **Requirements:**
    *   Must be declared as an approved delivery target within `promptops/delivery/`.
    *   Must meet stringent security, availability, and access control policies defined by the `@apastra/governance-admins`.
    *   Must enforce the same Acceptable Use policies and respond promptly to takedown requests.
    *   Must provide verified build provenance back to the origin repository.
