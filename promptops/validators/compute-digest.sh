#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

FILE=$1

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

EXT="${FILE##*.}"

if [ "$EXT" = "yaml" ] || [ "$EXT" = "yml" ]; then
    CANONICAL=$(yq '.' "$FILE" | jq -cSM .)
elif [ "$EXT" = "jsonl" ]; then
    CANONICAL=$(jq -cSM . "$FILE" | awk 'NR > 1 { printf "\n" } { printf "%s", $0 }')
elif [ "$EXT" = "json" ]; then
    CANONICAL=$(jq -cSM . "$FILE")
else
    echo "Error: Unsupported file extension '$EXT'."
    exit 1
fi

HASH=$(echo -n "$CANONICAL" | sha256sum | awk '{print $1}')

echo "sha256:$HASH"
