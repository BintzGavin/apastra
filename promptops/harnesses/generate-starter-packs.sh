#!/bin/bash
set -e

PACKS_DIR="derived-index/starter-packs"
TOPICS=("summarization" "extraction" "classification" "code-review")

echo "Generating starter packs in $PACKS_DIR..."

for topic in "${TOPICS[@]}"; do
    mkdir -p "$PACKS_DIR/$topic"

    cat << JSON_EOF > "$PACKS_DIR/$topic/pack.json"
{
  "id": "$topic-starter",
  "name": "Starter Pack: $topic",
  "description": "A curated starter pack for $topic tasks.",
  "custodian": "promptops-community",
  "prompts": ["$topic-prompt.yaml"],
  "datasets": ["$topic-dataset.json"],
  "evaluators": ["$topic-evaluator.yaml"],
  "suites": ["$topic-suite.yaml"],
  "baselines": [],
  "topics": ["$topic"]
}
JSON_EOF

    echo "Created starter pack for $topic."
done

echo "Starter packs generated successfully."
