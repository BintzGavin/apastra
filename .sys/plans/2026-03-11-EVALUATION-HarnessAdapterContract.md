#### 1. Context & Goal
- **Objective**: Spec the minimal harness adapter interface (input: run request; output: run artifact), plugin discovery, and error contract.
- **Trigger**: `README.md` describes a harness adapter contract (run request in → run artifact out), but `promptops/harnesses/` is empty.
- **Impact**: Unlocks the foundation for evaluation execution; GOVERNANCE gates depend on reproducible run artifacts produced by this contract.

#### 2. File Inventory
- **Create**: []
- **Modify**: []
- **Read-Only**:
  - `promptops/schemas/`
  - `README.md`

#### 3. Implementation Spec
- **Harness Architecture**:
  - The adapter must take a run request file and an output directory as inputs.
  - The adapter must output a structured run artifact directory.
  - The adapter must exit with a non-zero status code and emit structured failures if the run fails.
  - Plugin discovery is handled via a harness adapter definition file that specifies the invocation command and capabilities.
- **Run Request Format**: Must capture suite ID, revision reference (SHA/tag/digest), model matrix, trials, budgets, timeouts, evaluator references, and artifact backend configuration.
- **Run Artifact Format**: Must include a manifest (resolved digests, timestamps, status, harness version, model IDs, sampling config), a scorecard (normalized metrics, metric definitions, metric versioning, variance), per-case records with stable case IDs, raw artifact references (URIs and digests), and structured failures.
- **Pseudo-Code**:
  1. Parse input run request and output directory.
  2. Invoke RUNTIME resolver to resolve prompt package digest.
  3. Execute benchmark suite across datasets and model matrix.
  4. Collect metrics, raw text/traces, and evaluator outputs.
  5. Emit run artifact directory containing manifest, scorecard, per-case records, and artifact references.
  6. Return exit code 0 on success, or non-zero on failure with structured errors.
- **Baseline and Regression Flow**: Not applicable for this task.
- **Dependencies**:
  - CONTRACTS domain schemas: `harness-adapter.schema.json`, `run-request.schema.json`, `run-artifact.schema.json`.
  - RUNTIME domain: `promptops/resolver/chain.py`

#### 4. Test Plan
- **Verification**: `ls -al promptops/harnesses/`
- **Success Criteria**: The harness adapter contract is defined and allows CONTRACTS to build required schemas.
- **Edge Cases**: Missing RUNTIME resolver, invalid run request, evaluator failure.