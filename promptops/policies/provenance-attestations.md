# Provenance Attestations Policy

## Overview
This policy defines the handling, verification, and expectations of cryptographic signatures and build provenance attestations for prompt packages within the registry. It establishes clear, auditable rules for what constitutes valid provenance, ensuring supply-chain integrity for governed releases.

## Provenance Mechanisms
The registry relies on established supply-chain mechanisms for build provenance:
1. **SLSA-style Provenance**: Describes builder, invocation, and materials, asserting trust in the builder to record provenance correctly.
2. **GitHub Artifact Attestations**: Serves as the default mechanism for provenance if the custodian uses GitHub Actions as its build system.

## Verification and Enforcement
- **Signature Verification**: Valid signatures must be verified against approved builder identities.
- **Handling Unsigned Packages**: If a package lacks valid provenance attestations or signatures, the registry will flag the package as "unsigned/unverified".
- **Registry Behavior**: The registry will verify provenance attestations if provided, adhering to the standard publishing pipeline for bundle and OCI artifacts.
