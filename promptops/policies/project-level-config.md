# Project-Level Configuration Policy

## Purpose
This policy governs the global configuration defaults and the simplified minimal file structure auto-activation rules. It ensures consistent evaluation behavior and directory structure governance.

## Global Configuration (promptops.config.yaml)
If a promptops.config.yaml file exists in the repository root, its defined defaults act as the global baseline for all suites.
- **Inheritance**: Any suite that omits specific thresholds or configurations MUST inherit the defaults defined in this file.
- **Overrides**: Suites may explicitly override global defaults by defining their own values.
- **Review Requirement**: Any modifications to promptops.config.yaml require review and approval from @apastra/governance-admins to prevent unauthorized weakening of global thresholds.

## Simplified Minimal Mode
The "minimal mode" structure provides a simplified directory topology to reduce onboarding friction.
- **Structure**: Only prompts/, evals/, and baselines/ directories are utilized.
- **Auto-Activation**: Minimal mode is automatically activated for repositories containing ≤3 prompt specs.
- **Graduation**: Once a repository exceeds the 3 prompt spec limit, it must graduate from minimal mode to the full directory structure to maintain governance compliance.
