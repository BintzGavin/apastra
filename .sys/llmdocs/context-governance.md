**Section A: Schema Inventory**
- N/A

**Section B: Validator Inventory**
- N/A

**Section C: Source File Conventions**
- `.github/CODEOWNERS`:
  - `promptops/prompts/` @apastra/prompt-engineers
  - `promptops/schemas/` @apastra/governance-admins
  - `promptops/policies/` @apastra/governance-admins
  - `promptops/evaluators/` @apastra/evaluation-team
  - `promptops/suites/` @apastra/evaluation-team
  - `promptops/delivery/` @apastra/governance-admins
  - `derived-index/promotions/` @apastra/governance-admins
  - `.github/workflows/` @apastra/infrastructure
  - `.github/CODEOWNERS` @apastra/governance-admins

**Section D: Digest Convention**
- N/A

**Section E: Integration Points**
Promotion Record Format:
- `id`: Unique promotion event ID
- `timestamp`: ISO-8601 timestamp of promotion
- `digest`: The content digest of the promoted prompt package
- `channel`: Target distribution channel (e.g., "prod", "staging")
- `approver`: GitHub actor who approved/triggered the promotion
- `evidence_refs`: Array of URIs linking to regression reports or run artifacts
