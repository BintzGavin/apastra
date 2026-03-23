# Automated Scan Record Reference

A record of an automated scan performed on a prompt package.

## Properties

### `scan_id` (string, Required)
Unique identifier for this scan record.

### `package_digest` (string, Required)
The digest of the package that was scanned.

### `timestamp` (string, Required)
When the scan was performed.

### `scanner_id` (string, Required)
The tool or service performing the scan.

### `scan_type` (string, Required)
The type of scan performed.
**Enum values:** malware, secrets, schema, policy

### `result` (string, Required)
The outcome of the scan.
**Enum values:** pass, fail, warn

### `evidence_links` (array[string], Optional)
Optional links to detailed scan logs or evidence.

### `detailed_report` (string, Optional)
Optional detailed text report from the scanner.

