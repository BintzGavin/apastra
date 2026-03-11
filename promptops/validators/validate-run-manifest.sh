#!/bin/bash
FILE=$1
npx --yes ajv-cli validate -s promptops/schemas/run-manifest.schema.json -d "$FILE" --spec=draft2020 --strict=false
