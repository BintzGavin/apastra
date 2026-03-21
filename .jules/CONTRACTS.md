## 0.6.0 - Content Digest Convention
**Learning:** `jq` does not parse yaml files out of the box, `yq` is needed to correctly convert yaml to json for canonicalization in `compute-digest.sh`.
**Action:** Use `yq .` prior to piping to `jq` for any `.yaml` or `.yml` files.
## v0.60.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.61.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.67.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.73.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.74.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.75.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.76.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.77.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.78.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.79.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.80.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.81.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.82.0
- Executed Minimal Plan Exception Final for the CONTRACTS domain.
## v0.84.0
**Learning:** Foundational moderation primitives in `docs/vision.md` such as appeals require explicit schemas to enable the GOVERNANCE domain to operate effectively without hallucinating state.
**Action:** Always cross-reference high-level governance procedures (like takedowns and appeals) against existing schemas to ensure all states are representable.
## v0.85.0 - OwnershipDisputeRecord
**Learning:** `docs/vision.md` outlines policies for ownership disputes, which require a formalized schema for the GOVERNANCE domain to programmatically track and resolve claims.
**Action:** Ensure that all governance workflows explicitly listed in the vision document have a corresponding schema definition to prevent state hallucination.
## v0.86.0 - CommunityReportRecord
**Learning:** `docs/vision.md` specifically requires "community reporting" as part of the moderation path. Like other governance actions, this requires a formalized schema.
**Action:** Continue auditing moderation and governance concepts in the vision document to ensure there's a corresponding schema for each described procedure.
