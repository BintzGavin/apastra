# Appeals Policy

This policy governs the process for appealing moderation takedowns in the registry ecosystem.

## 1. Append-Only Records
Appeals are formally tracked as immutable `takedown-appeal-record.schema.json` artifacts in the registry metadata store.
In-place modification of past moderation decisions is strictly prohibited.

## 2. Appeal Workflow
The human checkpoint for overturning moderation decisions involves the following steps:
1. An appellant files an appeal, creating a new record with a `pending` status. This record must include reasoning and optional evidence links.
2. A human governance maintainer reviews the evidence provided in the appeal.
3. The maintainer appends a new record with the status updated to either `approved` or `rejected`.

## 3. Governance Boundary
Updates to this policy are governed by the `promptops/policies/ @apastra/governance-admins` boundary.

## 4. Edge Cases
Appeals filed after 30 days of the original takedown decision are automatically rejected, generating a corresponding append-only record with a `rejected` status.
