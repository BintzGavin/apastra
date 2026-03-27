#### 1. Context & Goal
- **Objective**: Establish governance policies for promoting specific model+prompt combinations from multi-model scorecards.
- **Trigger**: docs/vision.md explicitly states Multi-model promotion policies: governance rules for promoting a specific model+prompt combination from a multi-model comparison scorecard.
- **Impact**: Provides clear criteria for selecting and promoting the optimal model from a matrix of candidates based on quality, cost, and latency tradeoffs, creating an auditable decision record.

#### 2. File Inventory
- **Create**:
  - promptops/policies/multi-model-promotion.md: Governance policy defining how to evaluate multi-model scorecards and select candidates for promotion.
- **Modify**:
  - .github/CODEOWNERS: Add review requirements for promptops/policies/multi-model-promotion.md.
- **Read-Only**:
  - docs/vision.md

#### 3. Implementation Spec
- **Policy Architecture**: The policy will mandate that promotions from multi-model suites explicitly reference the selected model_id alongside the prompt digest. It will define criteria for acceptable tradeoffs (e.g., if model B is 5% lower quality but 50% cheaper, it requires specific review).
- **Workflow Design**: On PR or promotion request: If the suite uses a model_matrix, the promotion record MUST specify the chosen model_id. The workflow verifies the chosen model's scorecard metrics meet baseline thresholds.
- **CODEOWNERS Patterns**: /promptops/policies/multi-model-promotion.md @apastra/governance-admins
- **Promotion Record Format**: The policy will dictate that derived-index/promotions/<id>.json must include the selected model_id.
- **Delivery Target Format**: Delivery targets may need to be aware of the selected model.
- **Dependencies**: EVALUATION must generate scorecards that support multi-model results. CONTRACTS schemas for promotion records must support model_id.

#### 4. Test Plan
- **Verification**: Review the newly created governance document and CODEOWNERS update.
- **Success Criteria**: The policy document is created, explicitly detailing how to handle multi-model promotions, and is protected by CODEOWNERS.
- **Edge Cases**: Promotions from single-model suites should bypass these specific requirements.
