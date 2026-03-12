import sys, json
output_dir = sys.argv[2]
with open(f"{output_dir}/run_manifest.json", "w") as f:
    json.dump({"bad": "data"}, f)
