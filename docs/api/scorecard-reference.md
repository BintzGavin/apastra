# Scorecard Specification Reference

Schema for the run artifact scorecard.

## Properties

### `normalized_metrics` (object, Required)
Mapping of metric names to their values

### `metric_definitions` (object, Required)
Metadata like metric version and description

### `variance` (object, Optional)
Optional variance details if trials were run

### `flake_rates` (object, Optional)
Mapping of metric names to their flake rates

