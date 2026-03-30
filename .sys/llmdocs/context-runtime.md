# RUNTIME Domain Context

## Section A: Architecture
- **Resolution Chain**: local override -> workspace path -> git ref (SHA/tag) -> packaged artifact fallback.
- **Config**: Project config (`promptops.config.yaml`) defaults are merged into suites at execution.

## Section B: File Tree
```
promptops/
├── runtime/
│   ├── config.py
│   ├── index.py
│   ├── agent_skills.py
│   ├── resolve.py
│   └── runner.py
├── resolver/
│   ├── git_ref.py
│   ├── local.py
│   ├── packaged.py
│   └── workspace.py
```

## Section C: Public Interface
```python
def resolve(prompt_id: str, ref: str) -> dict: ...
def load_project_config() -> dict: ...
def apply_config_defaults(suite: dict, config: dict) -> dict: ...
def run_review_skill(prompt_spec_path: str) -> dict: ...
def run_red_team_skill(prompt_spec_path: str) -> list: ...
def run_optimize_skill(prompt_spec_path: str) -> dict: ...
```

## Section D: Manifest Format
Consumption manifest defines prompt versions per environment.

## Section E: Integration Points
EVALUATION uses `runner.py` to trigger harness execution. GOVERNANCE accesses resolving logic to audit prompts.
