---
title: "Promotion and Delivery Status"
description: "Implemented release boundaries and deferred delivery design"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - ".github/workflows/promote.yml"
  - ".github/workflows/deliver.yml"
---

# Promotion and Delivery Status

Apastra's supported release boundary is an evidence admission or regression decision. It does not implement downstream delivery, alerting or rollback.

The repository retains approval/promotion schemas and workflows as design scaffolding. Recording a promotion does not prove a target was updated. `deliver.yml` now fails explicitly, so callers cannot mistake an echo-only job for completed synchronization. The canary workflow likewise has no scheduled trigger and fails when manually invoked.

Use the admitted result as input to your existing deployment system. Keep its approvals, destination verification and rollback logic in that system until a tested Apastra integration exists. Signature verification is also unsupported; a digest alone is not an authenticated producer identity.

A future delivery integration must demonstrate an actual destination update, a verifiable receipt and failure behavior before its workflow can report success. No such integration is claimed by this candidate.
