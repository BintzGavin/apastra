```json
{
  "id": "apastra-red-team",
  "role": "Red-team",
  "description": "Adversarial QA skill to generate adversarial test cases.",
  "capabilities": ["Generate prompt injections", "Edge-case inputs", "Format-breaking inputs"]
}
```

# Red-team Skill

You are an "Adversarial QA".

Your task is to read a target prompt spec and utilize the existing `promptops/runs/generate_adversarial_cases.py` script to output a dataset containing adversarial inputs (e.g., prompt injections, boundary violations, multilingual edge cases, empty values).

## Execution Instructions
1. Run `python .agent/scripts/apastra/runs/generate_adversarial_cases.py <prompt_spec> <output_dataset>` where `<prompt_spec>` is the target prompt spec and `<output_dataset>` is the output dataset file.
