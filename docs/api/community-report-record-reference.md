# Community Report Record Reference

Schema for a community report record in the governance system.

## Properties

### `report_id` (string, Required)
Unique identifier for the report.

### `target_package_name` (string, Required)
The canonical name of the package or model being reported.

### `reporter_id` (string, Required)
Identifier of the party filing the report.

### `timestamp` (string, Required)
Timestamp when the report was created.

### `reason_category` (string, Required)
The categorization of the issue being reported.
**Enum values:** malware, hate_speech, pii_leak, spam, other

### `status` (string, Required)
Current status of the report.
**Enum values:** open, under_review, resolved

### `evidence_links` (array[string], Optional)
Optional list of URLs containing evidence supporting the report.

### `detailed_description` (string, Optional)
Optional detailed narrative explaining the report.

