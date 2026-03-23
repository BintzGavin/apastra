# Trusted Publisher Provenance Reference

Provenance record to verify and grant trusted publisher badges for packages and providers.

## Properties

### `publisher_id` (string, Required)
Unique identifier of the trusted publisher.

### `package_name` (string, Required)
Name or canonical digest of the package being published.

### `timestamp` (string, Required)
Time the provenance record was generated.

### `claims` (object, Required)
Verifications performed for trusted publisher badging.

