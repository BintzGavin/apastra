# Regression Report Specification Reference

Schema for a regression report output.

## Properties

### `status` (string, Required)
Pass, fail, warning status

### `baseline_ref` (string, Required)
The reference digest or ID

### `candidate_ref` (string, Required)
The digest or ID being tested

### `evidence` (array[object], Required)
A list of metric deltas and comparisons

