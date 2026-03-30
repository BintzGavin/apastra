import argparse
import yaml
import json
import sys
from promptops.runtime.resolve import resolve
from promptops.runtime.audit import scan_codebase

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        from promptops.runtime.mcp_server import start_mcp_server
        start_mcp_server()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "canary":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli canary")
        parser.add_argument("canary_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.canary import run_canary
        run_canary(args.canary_path)
        return

    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli compare")
        parser.add_argument("suite_id")
        parser.add_argument("--models", nargs="+")
        parser.add_argument("--adapter")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.compare import run_comparison
        scorecard = run_comparison(args.suite_id, args.models, args.adapter)
        print(json.dumps(scorecard, indent=2))
        return


    if len(sys.argv) > 1 and sys.argv[1] == "audit":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli audit")
        parser.add_argument("directory", nargs="?", default=".")
        args = parser.parse_args(sys.argv[2:])
        report = scan_codebase(args.directory)
        print(json.dumps(report, indent=2))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "apastra-review":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli apastra-review")
        parser.add_argument("prompt_spec_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.agent_skills import run_review_skill
        report = run_review_skill(args.prompt_spec_path)
        print(json.dumps(report, indent=2))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "apastra-red-team":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli apastra-red-team")
        parser.add_argument("prompt_spec_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.agent_skills import run_red_team_skill
        cases = run_red_team_skill(args.prompt_spec_path)
        print(json.dumps(cases, indent=2))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "apastra-optimize":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli apastra-optimize")
        parser.add_argument("prompt_spec_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.agent_skills import run_optimize_skill
        suggestions = run_optimize_skill(args.prompt_spec_path)
        print(json.dumps(suggestions, indent=2))
        return


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
