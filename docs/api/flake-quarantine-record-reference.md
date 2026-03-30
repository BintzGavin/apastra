# Flake Quarantine Record

**Schema**: `flake-quarantine-record.schema.json`
**Description**: A record that tracks and quarantines a flaky evaluation case.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | Yes | Stable identifier for the quarantine record. |
| `case_id` | `string` | Yes | The ID of the dataset case being quarantined. |
| `suite_id` | `string` | Yes | The ID of the suite where the case flakes. |
| `evaluator_id` | `string` | Yes | The evaluator that produced the flaky result. |
| `flake_rate` | `number` | Yes | A number representing the observed flake rate. |
| `timestamp` | `string` (date-time) | Yes | The timestamp when the case was quarantined. |
| `reason` | `string` | Yes | Explanation of why the case was quarantined. |
| `status` | `string` | Yes | The current status of the quarantine (e.g., active, resolved). |

## Example

```json
{
  "id": "quar-12345",
  "case_id": "case-abc",
  "suite_id": "suite-def",
  "evaluator_id": "eval-ghi",
  "flake_rate": 0.25,
  "timestamp": "2023-10-01T12:00:00Z",
  "reason": "Fails intermittently on latency checks.",
  "status": "active"
}
```
