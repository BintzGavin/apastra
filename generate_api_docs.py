import json
import os
from datetime import datetime

date_str = "2026-03-11"

def generate_markdown(schema_file, output_file):
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    title = schema.get('title', os.path.basename(schema_file).replace('.schema.json', '').replace('-', ' ').title())
    description = schema.get('description', f"API reference for {title}")

    md_content = f"""---
title: "{title} Reference"
description: "{description}"
audience: "developers | platform-teams | agents | all"
last_verified: "{date_str}"
source_files:
  - "{schema_file}"
---

# {title} Reference

{description}

"""
    def parse_properties(properties, required, level=2):
        res = ""
        for prop, details in properties.items():
            req_str = "Required" if prop in required else "Optional"
            prop_type = details.get('type', 'any')

            if '$ref' in details:
                prop_type = "object"
            elif prop_type == 'array':
                items = details.get('items', {})
                if '$ref' in items:
                    prop_type = f"array of objects"
                else:
                    prop_type = f"array of {items.get('type', 'any')}"

            desc = details.get('description', '')
            res += f"{'#' * level} `{prop}`\n\n"
            res += f"- **Type:** {prop_type}\n"
            res += f"- **Requirement:** {req_str}\n"
            if desc:
                res += f"- **Description:** {desc}\n"

            if 'enum' in details:
                res += f"- **Allowed Values:** {', '.join([str(x) for x in details['enum']])}\n"

            res += "\n"

            if prop_type == 'object' and 'properties' in details:
                res += parse_properties(details['properties'], details.get('required', []), level + 1)

            if 'items' in details and 'properties' in details['items']:
                res += parse_properties(details['items']['properties'], details['items'].get('required', []), level + 1)

        return res

    if 'properties' in schema:
        md_content += "## Properties\n\n"
        md_content += parse_properties(schema['properties'], schema.get('required', []))

    with open(output_file, 'w') as f:
        f.write(md_content)

os.makedirs('docs/api', exist_ok=True)
schemas = [f for f in os.listdir('promptops/schemas') if f.endswith('.json')]
for schema in schemas:
    schema_path = os.path.join('promptops/schemas', schema)
    output_path = os.path.join('docs/api', schema.replace('.schema.json', '-reference.md'))
    generate_markdown(schema_path, output_path)

print("Generated API docs")
