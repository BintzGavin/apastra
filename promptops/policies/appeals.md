# Takedown Appeals Policy

## Purpose
This policy establishes a formal, append-only process for content authors or package owners to appeal decisions made by the Governance Team regarding content takedowns.

## Eligibility
Only the original author or designated package owner of a prompt package that has been subject to a moderation takedown action can submit an appeal.

## Appeal Process and Append-Only Registry
Appeals against takedown decisions are governed via the append-only registry metadata store. Historical appeal claims **MUST NEVER** be modified or deleted in-place.

To submit an appeal, the creation of a `takedown-appeal-record` JSON artifact is mandated. The record must contain the following required fields:
- `appeal_id`: Unique identifier for the appeal.
- `takedown_record_id`: Reference to the original takedown record being appealed.
- `appellant_id`: Identifier of the user or entity filing the appeal.
- `reasoning`: Text reasoning explaining why the takedown should be overturned.
- `status`: Current status of the appeal. The initial state of the record **MUST** be `pending`.

When supplying new contextual evidence, `evidence_links` is the preferred mechanism and should be included in the artifact.

## Review Process
1. **Receipt**: The Governance Team will acknowledge the appeal and verify the `pending` `takedown-appeal-record`.
2. **Independent Assessment**: The appeal will be assigned to a Governance Team member not involved in the original moderation decision to ensure impartiality. They will assess the new evidence against the Acceptable Use Policy and original findings.
3. **Final Decision**: The reviewer will make a final determination. This independent assessment results in a **subsequent** `takedown-appeal-record` being appended to transition the state to `approved` (upholding the appeal and overturning the takedown) or `rejected` (denying the appeal and upholding the takedown).

## Finality
Decisions reached through the appeal process and recorded as `approved` or `rejected` are considered final and binding. Repeatedly appealing the same decision without new evidence is considered a violation of community guidelines.
