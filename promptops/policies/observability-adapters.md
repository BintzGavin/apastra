# Observability Adapters Policy

## Purpose
Establish a policy governing the integration and behavior of observability bridge adapters within the promptops ecosystem.

## Adapter Registration
All observability adapters must be explicitly defined and registered in `promptops/delivery/observability.yaml`.

## Credential Management
Adapters are strictly prohibited from hardcoding credentials. All sensitive credentials must be injected dynamically via environment variables supplied securely by the runner.

## Resilience
Adapters must gracefully handle network failures, timeouts, and upstream outages. An adapter failure must not crash or halt the core prompt execution run or the evaluation process.
