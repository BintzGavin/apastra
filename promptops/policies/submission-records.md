# Submission Records Policy

## 1. Overview
The registry relies on submission records to document every prompt package submitted. This ensures an auditable and traceable history from initial submission to final publish.

## 2. Append-Only Requirement
Submission records must be strictly append-only. They serve as the immutable ledger mapping for the registry.

## 3. Required Metadata
Every submission record must contain the following metadata:
- The deterministic digest of the submitted package
- The schema validation status
- The results of automated policy scans
- Cryptographic build provenance attestations
- The identity of the author or publisher

## 4. Moderation and Publishing Lineage
All downstream actions, including moderation decisions (flags, approvals, or rejections) and publishing events, must explicitly link back to this immutable submission record.
