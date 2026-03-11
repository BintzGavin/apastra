# SECTION A: Guide Inventory

| Title | Audience | Last Verified |
|---|---|---|
| Architecture Overview | developers \| platform-teams \| agents \| all | 2026-03-11 |
| Getting Started | developers \| platform-teams \| agents \| all | 2026-03-11 |
| Repo Topology | developers \| platform-teams \| agents | 2026-03-11 |
| Black Hole Architecture | developers \| platform-teams \| agents | 2026-03-11 |
| Harness Contract | developers \| platform-teams \| agents | 2026-03-11 |
| Consumption and Resolution | developers \| platform-teams \| agents | 2026-03-11 |
| Promotion and Delivery | developers \| platform-teams \| agents | 2026-03-11 |

# SECTION B: API Reference Inventory

| Schema File | Path |
|---|---|
| prompt-spec.schema.json | docs/api/prompt-spec-reference.md |
| dataset-manifest.schema.json | docs/api/dataset-manifest-reference.md |
| dataset-case.schema.json | docs/api/dataset-case-reference.md |
| evaluator.schema.json | docs/api/evaluator-reference.md |
| suite.schema.json | docs/api/suite-reference.md |
| consumption-manifest.schema.json | docs/api/consumption-manifest-reference.md |
| run-request.schema.json | docs/api/run-request-reference.md |
| run-artifact.schema.json | docs/api/run-artifact-reference.md |
| harness-adapter.schema.json | docs/api/harness-adapter-reference.md |

# SECTION C: ADR Inventory

| ID | Title | Status |
|---|---|---|
| ADR 001 | Git-Native Control Plane | Accepted |
| ADR 002 | Bring-Your-Own Harnesses | Accepted |
| ADR 003 | Content Digest Identity | Accepted |

# SECTION D: Dashboard Inventory

| Dashboard | Path |
|---|---|
| Domain Status Overview | docs/dashboards/domain-status-overview.md |
| Implementation Progress | docs/dashboards/implementation-progress.md |
| Schema Dependency Graph | docs/dashboards/schema-dependency-graph.md |

# SECTION E: Coverage Gaps

* Missing schemas from pending domains (e.g., `baseline.schema.json`, `regression-policy.schema.json`, `regression-report.schema.json`, `delivery-target.schema.json`, `promotion-record.schema.json`) will need API docs once implemented.
* Future guides may be needed for specific evaluator patterns and CI/CD setup once more mature.
