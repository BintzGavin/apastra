# Moderation Approval for Public Listing

## 1. Overview
This policy defines the formal human checkpoint required before any asset is permitted to be publicly listed in the registry. It ensures that standard automated checks are supplemented by explicit, auditable human review to enforce moderation standards.

## 2. Scope
This policy applies to all prompts, datasets, and evaluators submitted for public listing in the registry metadata store.

## 3. Human Approval Process
- **Prerequisites:** All automated policy and regression checks must pass.
- **Review Requirement:** A designated moderator must explicitly review the content against the `moderation-policy.md` guidelines.
- **Decision Recording:** The outcome (approval or rejection) must be recorded as an append-only entry following the `moderation-decision-records.md` format.

## 4. Enforcement
Assets lacking a verified moderation approval record cannot be transitioning to a public listing state.
