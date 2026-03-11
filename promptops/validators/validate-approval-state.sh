#!/bin/bash
npx ajv-cli validate -s promptops/schemas/approval-state.schema.json -d "$1" --spec=draft2020 --strict=false -c ajv-formats
