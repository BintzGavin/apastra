# Moderation Escalation Path Policy

This policy governs the human escalation path for high-risk content within the registry, ensuring that all escalations are formally recorded, reviewed, and auditable in accordance with the `moderation-escalation-record.schema.json`.

## 1. Context and Scope
When automated moderation systems or community reports identify content that represents a severe or ambiguous risk (e.g., safety, IP, privacy, authenticity), standard review timelines are insufficient. This policy mandates the creation of append-only `moderation-escalation-record` files when such high-risk escalations occur, guaranteeing a human checkpoint before final disposition.

## 2. Trigger Conditions
An escalation is triggered either manually by a moderator encountering complex, high-risk content, or automatically when specific high-risk flags are raised by validation workers.

## 3. The Moderation Escalation Record
Every escalation MUST result in a durable, append-only record conforming to the `moderation-escalation-record.schema.json`.

### Required Fields
- `escalation_id`: A unique identifier for the escalation.
- `submission_id`: The unique identifier for the prompt package submission being escalated.
- `escalated_by`: The identifier of the user or automated system that escalated the content.
- `reason`: A detailed string explaining the reason for the escalation (e.g., "Potential severe safety violation").
- `timestamp`: The date-time of the escalation.
- `status`: The current status of the escalation (`pending`, `reviewed`, `dismissed`).

### Optional Fields
- `reviewer_id`: The identifier of the human reviewer who handled the escalation (required if status is `reviewed` or `dismissed`).
- `notes`: Additional notes regarding the escalation context or resolution.

## 4. Workflow and Review Boundaries
- **Invocation:** Escalations are initiated by creating a `moderation-escalation-record` with a `pending` status.
- **Review Requirement:** Only members defined in the CODEOWNERS pattern for governance policies (e.g., `@apastra/governance-admins`) are authorized to review and resolve escalations.
- **Resolution:** A reviewer must update the record's status to `reviewed` or `dismissed` and append a new record if necessary, maintaining append-only lineage. The `reviewer_id` must be populated upon resolution.
