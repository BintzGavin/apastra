# Namespace Claims Policy

This policy governs the registration, tracking, and dispute resolution of canonical namespaces in the registry.

## Registration and Append-Only Tracking
All namespace claims are tracked exclusively using append-only `namespace-claim-record` JSON artifacts in the registry metadata store.
- The append-only chain of `namespace-claim-record` artifacts forms the single source of truth for all namespace registrations.
- Historical claims MUST NEVER be modified or deleted in-place. All updates, such as status transitions, are handled by appending new records.
- A valid claim submission must include a `claim_id`, the requested `namespace`, the `requester_id`, and a `timestamp`.

## Moderation and Human Checkpoints
Namespace claims require human moderation checkpoints to transition statuses:
- `pending`: The initial state of a submitted namespace claim.
- `approved`: Moderation has reviewed and granted the namespace claim.
- `rejected`: Moderation has denied the namespace claim.
- `disputed`: The namespace is actively contested by another party.

## Ownership and Trademark Verification
When disputing or claiming a protected namespace, users MUST provide an `evidence_uri` pointing to verifiable proof of ownership, trademark documentation, or prior art.
