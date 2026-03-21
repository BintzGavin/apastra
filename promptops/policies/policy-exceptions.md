# Policy Exceptions

## Objective
Establish a formal and auditable human escalation path to override blocking governance checks, providing flexibility for edge cases while ensuring strict oversight.

## Criteria and Process
Any exception to an automated block requires explicit human review. Approved exceptions must be recorded as append-only records in the registry metadata store.

Users must submit a GitHub issue requesting an exception. A designated approver from the `@apastra/governance-admins` team must review and approve. Once approved, an append-only exception record will be recorded.
