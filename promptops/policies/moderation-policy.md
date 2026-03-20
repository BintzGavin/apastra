# Moderation and Policy Checks

## 1. Overview
This policy defines the criteria for moderation and policy check failures, automated scanning requirements, and the human escalation path for manual flagging of prompt packages to secure the registry ecosystem.

## 2. Automated Scanning
All submissions will undergo automated scanning for:
- Schema validation
- Secrets detection
- Obvious policy checks (e.g., unacceptable use keywords)

Failures in automated scanning will automatically block downstream delivery and apply an immutable failure flag to the registry metadata store.

## 3. Moderation Failure Criteria
A prompt package may be flagged for moderation failure if it violates the constraints outlined in `acceptable-use.md` or presents high-risk content that compromises safety, IP, privacy, or authenticity.

## 4. Human Escalation Path
High-risk content or community reports will trigger a human escalation path.
- Moderation admins will review the content.
- If a moderation failure is confirmed manually, the admin will append an immutable failure flag to the registry metadata store, preventing consumption.
- Users can query the flag status before usage.

## 5. Metadata Flags
Flags appended to the registry metadata store must clearly indicate the reason for failure (e.g., "automated-secret-scan-failed", "manual-moderation-flag") and remain immutable to provide an auditable trail.
