# Trusted Publisher Policy

## Objective
To establish a verifiable mechanism to grant "trusted publisher" status based on cryptographically signed build provenance, increasing ecosystem security and trust.

## Definition
A "trusted publisher" is an entity (organization or individual) whose prompt packages have been cryptographically verified to originate from an approved source repository using secure build pipelines.

## Requirements for Trusted Publisher Badge
1. **Provenance Verification**: Packages must be published with valid SLSA/GitHub artifact attestations linking back to an approved organization/repository.
2. **Moderation Scans**: Submissions must pass automated moderation scans (schema validation, secrets detection, policy checks).
3. **Acceptable Use Policy**: Packages must adhere strictly to the Acceptable Use Policy.