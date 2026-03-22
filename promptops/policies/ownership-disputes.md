# Ownership Disputes Policy

This policy defines the process for managing ownership disputes over canonical prompt package namespaces in the public registry. To ensure transparency, auditability, and historical integrity, all ownership disputes are tracked via an append-only registry metadata store using the `ownership-dispute-record` schema.

## 1. Dispute Initiation
- When a dispute is reported, a new `ownership-dispute-record.schema.json` artifact MUST be created and appended to the registry metadata store.
- The initial record MUST have the status `open`.
- The record MUST include the `dispute_id`, `package_name`, `complainant_id`, `timestamp`, and a detailed `claim_reason`.
- Evidence of original authorship or trademark rights MUST be provided via `evidence_links`.

## 2. Investigation Phase
- As the moderation team reviews the claim, a new, distinct `ownership-dispute-record` MUST be appended reflecting the state transition to `under_review`.
- Historical dispute claims MUST NEVER be modified or deleted in-place. All updates are handled by appending new records.

## 3. Resolution Phase
- Upon reaching a decision, a final `ownership-dispute-record` MUST be appended with the status `resolved`.
- The `resolution_notes` field MUST detail the rationale for the decision.
- If an original owner is unresponsive for 14 business days, or a package is definitively abandoned, the namespace MAY be transferred to the complainant, with the transfer documented via an appended resolution record.

## 4. Immutability & Audit
- Deletion of historical dispute records is strictly prohibited.
- The append-only chain of `ownership-dispute-record` artifacts forms the single source of truth for all namespace ownership conflicts.
