import argparse
import yaml
from promptops.runtime.resolve import resolve

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_id")
    parser.add_argument("--ref", default=None)
    parser.add_argument("--emit-manifest", action="store_true")
    args = parser.parse_args()

    rendered, metadata = resolve(args.prompt_id, args.ref)
    print("--- Resolved Template ---")
    print(rendered)

    if args.emit_manifest:
        entry_type = "override" if args.ref and ('/' in args.ref or '\\' in args.ref) else "pin"
        ref_val = args.ref if args.ref else "latest"
        snippet = {"version": "1.0", "prompts": {args.prompt_id: {"id": args.prompt_id, entry_type: ref_val}}}
        print("--- Manifest Entry ---")
        print(yaml.dump(snippet, sort_keys=False))

if __name__ == "__main__":
    main()
