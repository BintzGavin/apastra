import argparse
import yaml
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    import importlib
    package = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(package.parent))
    sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.resolve import resolve
from promptops.runtime.audit import scan_codebase

def _main():
    if len(sys.argv) > 1 and sys.argv[1] == "ci-gate":
        from promptops.runtime.ci import ci_gate
        parser = argparse.ArgumentParser(prog="apastra ci-gate")
        parser.add_argument("suite")
        parser.add_argument("--adapter", required=True)
        parser.add_argument("--revision", required=True)
        parser.add_argument("--mode", choices=("execute", "evidence"), required=True)
        parser.add_argument("--run-dir", required=True)
        parser.add_argument("--baseline")
        parser.add_argument("--policy")
        args = parser.parse_args(sys.argv[2:])
        result = ci_gate(args.suite, args.adapter, args.revision, args.mode, args.run_dir, args.baseline, args.policy)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["status"] == "pass" else 2

    if len(sys.argv) > 1 and sys.argv[1] in {"gate", "baseline", "validate", "digest"}:
        from pathlib import Path
        from promptops.runtime.digest import compute_digest, load_asset
        from promptops.runtime.suite import validate_asset
        command = sys.argv[1]
        parser = argparse.ArgumentParser(prog=f"apastra {command}")
        if command in {"validate", "digest"}:
            if command == "validate":
                parser.add_argument("kind", choices=[path.name.removesuffix(".schema.json") for path in (Path(__file__).parents[1] / "schemas").glob("*.schema.json")])
            parser.add_argument("path")
            args = parser.parse_args(sys.argv[2:])
            if command == "validate":
                data = load_asset(args.path)
                if Path(args.path).suffix == ".jsonl" and not data:
                    raise ValueError("Dataset must contain at least one case")
                for row in data if Path(args.path).suffix == ".jsonl" else [data]:
                    validate_asset(row, args.kind)
                result = {"status": "valid"}
            else:
                result = {"digest": compute_digest(args.path)}
            print(json.dumps(result))
            return 0
        from promptops.runtime.gate import admit_run, establish_baseline, regression
        if command == "baseline":
            parser.add_argument("suite_id")
            parser.add_argument("name")
            parser.add_argument("run_dir")
        else:
            parser.add_argument("run_dir")
            parser.add_argument("--baseline")
            parser.add_argument("--policy")
            parser.add_argument("--revision")
            parser.add_argument("--suite")
            parser.add_argument("--check-workspace", action="store_true")
            parser.add_argument("--output")
        parser.add_argument("--adapter", required=True)
        args = parser.parse_args(sys.argv[2:])
        if command == "baseline":
            result = establish_baseline(args.suite_id, args.name, args.run_dir, args.adapter)
        elif args.baseline or args.policy:
            if not args.baseline or not args.policy:
                parser.error("Regression requires both --baseline and --policy")
            result = regression(args.run_dir, args.baseline, args.policy, args.adapter, args.revision, args.suite, args.check_workspace)
        else:
            result = admit_run(args.run_dir, args.adapter, args.revision, args.suite, args.check_workspace)["decision"]
        if command == "gate" and args.output:
            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2, allow_nan=False)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["status"] == "pass" else 2

    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        from promptops.runtime.mcp_launcher import main as mcp_main
        return mcp_main(sys.argv[2:])

    if len(sys.argv) > 1 and sys.argv[1] == "canary":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli canary")
        parser.add_argument("canary_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.canary import run_canary
        print(json.dumps(run_canary(args.canary_path)))
        return 3

    if len(sys.argv) > 1 and sys.argv[1] in {"eval", "compare", "quick-eval"}:
        command = sys.argv[1]
        parser = argparse.ArgumentParser(prog=f"apastra {command}")
        parser.add_argument("suite_id")
        parser.add_argument("--models", nargs="+")
        parser.add_argument("--adapter", required=True)
        parser.add_argument("--output-dir")
        args = parser.parse_args(sys.argv[2:])
        if command == "compare":
            from promptops.runtime.compare import run_comparison
            result = run_comparison(args.suite_id, args.models, args.adapter, args.output_dir)
        elif command == "quick-eval":
            from promptops.runtime.quick import evaluate_quick
            result = evaluate_quick(args.suite_id, args.models, args.adapter, args.output_dir)
        else:
            from promptops.runtime.suite import evaluate_suite
            result = evaluate_suite(args.suite_id, args.adapter, args.output_dir, models=args.models)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["status"] == "pass" else 2


    if len(sys.argv) > 1 and sys.argv[1] == "audit":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli audit")
        parser.add_argument("directory", nargs="?", default=".")
        args = parser.parse_args(sys.argv[2:])
        report = scan_codebase(args.directory)
        print(json.dumps(report, indent=2))
        return
    if len(sys.argv) > 1 and sys.argv[1] in {"apastra-review", "apastra-optimize"}:
        parser = argparse.ArgumentParser(prog=f"apastra {sys.argv[1]}")
        parser.error("Automated prompt analysis is not implemented. Use the Apastra skill workflows for review and optimization.")

    if len(sys.argv) > 1 and sys.argv[1] == "apastra-red-team":
        parser = argparse.ArgumentParser(prog="promptops.runtime.cli apastra-red-team")
        parser.add_argument("prompt_spec_path")
        args = parser.parse_args(sys.argv[2:])
        from promptops.runtime.agent_skills import run_red_team_skill
        cases = run_red_team_skill(args.prompt_spec_path)
        print(json.dumps(cases, indent=2))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "resolve":
        sys.argv.pop(1)
    parser = argparse.ArgumentParser(
        prog="apastra",
        description="Git-native evaluation and evidence admission. Requires an explicit measured adapter for execution.",
        epilog="Commands: resolve, eval, quick-eval, compare, gate, ci-gate, baseline, validate, digest, mcp, audit, request-log. Use COMMAND --help for its arguments. A bare prompt ID retains legacy resolution behavior.",
    )
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

def main():
    try:
        return _main()
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, yaml.YAMLError) as error:
        print(json.dumps({"status": "error", "reason": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
