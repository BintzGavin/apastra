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
## 0.93.0 - ProvenanceAttestation
**Learning:** `docs/vision.md` lists "Provenance attestations" as a core append-only artifact required for governed releases and supply-chain integrity, meaning it requires its own formal contract schema independent of existing tracking records.
**Action:** When a vision requirement details specific immutable metadata (like SLSA-style builder/invocation fields), ensure a distinct schema exists so downstream domains can accurately generate and validate these records.
## 0.94.0 - ProvenanceAttestation
**Learning:** `docs/vision.md` explicitly defines "Provenance attestations" as core artifacts for establishing supply-chain provenance. The creation of a dedicated schema allows for standardized issuance, attachment, and verification across domains.
**Action:** Always formalize architectural concepts from the vision document into explicit schema implementations to enable proper cross-domain interaction.
## 0.95.0 - PolicyExceptionRecord
**Learning:** `docs/vision.md` explicitly defines "Policy exceptions" as human checkpoints for moderation approval. Like other governance actions, an explicit schema is required so downstream domains can accurately generate and validate these records.
**Action:** Always formalize architectural concepts from the vision document into explicit schema implementations to enable proper cross-domain interaction.
## 0.97.0 - ModerationEscalationRecord
**Learning:** `docs/vision.md` explicitly defines a "human escalation path for high-risk content" as part of the public registry moderation procedures. The creation of a dedicated schema is required for the system to formally track these human escalations without hallucinating state.
**Action:** Continue cross-referencing high-level moderation procedures against existing schemas to ensure all documented states have an explicit schema definition for downstream domains.
## 0.98.0 - EmergencyTakedownDecision
**Learning:** `docs/vision.md` outlines "Emergency takedown decisions" as a human checkpoint. A specific schema is required to formalize these high-priority administrative actions without hallucinating state.
**Action:** Continue to audit all governance checkpoints and moderation procedures in the vision document to guarantee all procedural steps have explicit schema representations.
## 0.99.0 - ModerationApprovalForPublicListing
**Learning:** `docs/vision.md` outlines "Moderation approval for public listing" as a human checkpoint. Like other governance actions, an explicit schema is required so downstream domains can accurately generate and validate these records.
**Action:** Continue to audit all governance checkpoints and moderation procedures in the vision document to guarantee all procedural steps have explicit schema representations.
## 1.0.0 - DeliveryTargetReceipt
**Learning:** `docs/vision.md` explicitly defines a "delivery target receipt" as the final step of the prompt revision lineage trace. A dedicated schema is required to correctly validate and formalize these records downstream without hallucinating state.
**Action:** Audit and ensure all lineage trace end states defined in the vision document have explicit schema representations.
