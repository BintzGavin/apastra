# Artifact Storage & Retention Policy

## Purpose
To ensure the long-term auditability, durability, and compliance of derived artifacts (e.g., traces, full cases.jsonl, run manifests), overriding the default ephemeral nature of CI/CD compute environments.

## Policy Rules
1. Compute Layer Ephemerality: GitHub Actions (or any equivalent CI/CD runner) is strictly the compute layer. Artifacts stored natively in GitHub Actions default to a 90-day retention period and MUST NOT be treated as the long-term archive.
2. Long-Term Retention: All critical derived artifacts required for audit replay, compliance, or historical baselining MUST be synced to an external object store (e.g., AWS S3, Google Cloud Storage) or an OCI registry.
3. Auditability: The long-term archive MUST maintain an append-only structure. Artifacts MUST be indexed by their deterministic content digest and run ID to guarantee reproducibility.
4. Enforcement: Automated delivery or promotion workflows SHOULD verify that long-term syncing has occurred before marking a release as fully governed.
