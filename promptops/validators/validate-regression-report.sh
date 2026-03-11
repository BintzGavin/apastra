#!/bin/bash
FILE=$1
npx ajv-cli validate -s promptops/schemas/regression-report.schema.json -d "$FILE" --spec=draft2020 --strict=false