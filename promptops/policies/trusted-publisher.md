# Trusted Publisher Policy

## Objective
To establish a verifiable mechanism to grant "trusted publisher" status based on cryptographically signed build provenance, increasing ecosystem security and trust. This status is governed via the append-only registry metadata store.

## Definition
A "trusted publisher" is an entity (organization or individual) whose prompt packages have been cryptographically verified to originate from an approved source repository using secure build pipelines.

## Requirements for Trusted Publisher Badge
1. **Provenance Verification**: Packages must be published with valid SLSA/GitHub artifact attestations linking back to an approved organization/repository. This requires the creation of an append-only `trusted-publisher-provenance` JSON artifact containing `publisher_id`, `package_name`, `timestamp`, and `claims`.
   - The `claims` object MUST record verification statuses for:
     - `identity_verified`
     - `source_repo_linked`
     - `build_environment_attested`
2. **Moderation Scans**: Submissions must pass automated moderation scans (schema validation, secrets detection, policy checks).
3. **Acceptable Use Policy**: Packages must adhere strictly to the Acceptable Use Policy.
4. **Append-Only Rule**: Historical provenance claims MUST NEVER be modified or deleted in-place. If trusted publisher status is revoked or claims are updated, a new provenance record MUST be appended.
