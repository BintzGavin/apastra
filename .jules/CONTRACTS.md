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
## 0.88.0 - AutomatedScanRecord
**Learning:** `docs/vision.md` requires "automated scanning (schema validation, secrets detection, obvious policy checks)" as a prerequisite for moderation, necessitating a formalized schema for scan records.
**Action:** Continuously audit the vision document's moderation and governance workflows to guarantee all procedural steps have explicit schema representations, preventing state hallucination by the GOVERNANCE domain.
## 0.89.0 - TrustedPublisherProvenance
**Learning:** `docs/vision.md` outlines "trusted publisher" badges that require verifiable provenance requirements (e.g., identity, build environment, and source). A specific schema is needed to represent this provenance metadata accurately.
**Action:** When a vision requirement (like trusted publisher badges) involves verifiable claims, explicitly define the underlying schema structure to serve as the contract for generating and validating those claims.
## 0.90.0 - VulnerabilityFlagRecord
**Learning:** `docs/vision.md` outlines "vulnerability flags" as part of the append-only registry metadata store, which requires a formalized schema for the GOVERNANCE domain to programmatically track and enforce.
**Action:** Continue auditing moderation and governance concepts in the vision document to ensure there's a corresponding schema for each described procedure, preventing state hallucination.
## 0.91.0 - NamespaceClaimRecord
**Learning:** `docs/vision.md` mandates a transparent governance policy for "naming" in the registry. Like ownership disputes, this requires a formalized schema for claiming namespaces.
**Action:** Ensure all governance concepts related to registry namespace and identity explicitly listed in the vision document have a corresponding schema definition.
