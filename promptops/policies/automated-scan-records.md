# Automated Scan Records Policy

This policy governs the creation and storage of automated scan records, ensuring all prompt packages are verified against baseline security and policy requirements in an auditable, append-only manner. This aligns with the `automated-scan-record.schema.json`.

## 1. Context and Scope
As required by the registry's moderation procedures, all submitted packages must undergo automated scanning for schema validation, secrets detection, and obvious policy checks (e.g., unacceptable use keywords). This policy dictates how the results of these scans are durably recorded in the append-only registry metadata store.

## 2. Trigger Conditions
An automated scan record MUST be generated every time a prompt package undergoes automated evaluation by the registry's ingestion pipeline or background workers.

## 3. The Automated Scan Record
Every automated scan MUST result in a durable, append-only record conforming to the `automated-scan-record.schema.json`.

### Required Fields
- `scan_id`: A unique identifier for the scan execution.
- `package_digest`: The content digest of the prompt package that was scanned.
- `timestamp`: The date-time the scan was performed.
- `scanner_id`: The identifier of the tool or service performing the scan.
- `scan_type`: The category of the scan (`malware`, `secrets`, `schema`, `policy`).
- `result`: The outcome of the scan (`pass`, `fail`, `warn`).

### Optional Fields
- `evidence_links`: URLs linking to detailed scan logs or external evidence.
- `detailed_report`: A detailed text summary of the scan findings.

## 4. Immutability and State
Automated scan records are strictly append-only.
- If a subsequent scan is performed (e.g., due to updated scanning signatures), a new `automated-scan-record` MUST be appended.
- Historical scan records MUST NEVER be modified or deleted in-place.
- A `fail` result automatically blocks downstream delivery and flags the package in the metadata store.
