# Community Report Records Policy

This policy governs the creation and storage of community report records, formalizing community moderation within the append-only registry metadata store and aligning with the `community-report-record.schema.json`.

## 1. Context and Scope
As required by `docs/vision.md`, the registry's moderation procedures must require "community reporting". This policy dictates how community reports regarding prompt packages or models are durably recorded to support an actionable moderation queue.

## 2. Trigger Conditions
A community report record MUST be generated when a user or automated agent files a report against a public registry package through the designated reporting workflow.

## 3. The Community Report Record
Every community report MUST result in a durable, append-only record conforming to the `community-report-record.schema.json`.

### Required Fields
- `report_id`: A unique identifier for the report.
- `target_package_name`: The canonical name of the package or model being reported.
- `reporter_id`: The identifier of the party filing the report.
- `timestamp`: The date-time the report was created.
- `reason_category`: The category of the issue (`malware`, `hate_speech`, `pii_leak`, `spam`, `other`).
- `status`: The current status of the report (`open`, `under_review`, `resolved`).

### Optional Fields
- `evidence_links`: URLs linking to external evidence supporting the report.
- `detailed_description`: A detailed text narrative explaining the report.

## 4. Immutability and State Transitions
Community report records are strictly append-only.
- If a moderation decision is made, a subsequent `moderation-decision-record` or an updated `community-report-record` (depending on the workflow specifics) MUST be appended.
- Historical report records MUST NEVER be modified or deleted in-place.
- A status transition from `open` to `resolved` requires a new appended record reflecting the new state.
