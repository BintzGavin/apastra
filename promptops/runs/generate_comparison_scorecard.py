import json
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_comparison_scorecard.py <output_path> <scorecard_path_1> [<scorecard_path_2> ...]")
        sys.exit(1)

    output_path = sys.argv[1]
    scorecard_paths = sys.argv[2:]

    comparison = {}

    for path in scorecard_paths:
        with open(path, 'r') as f:
            data = json.load(f)

        model_id = os.path.basename(os.path.dirname(path))
        comparison[model_id] = data

    with open(output_path, 'w') as f:
        json.dump(comparison, f, indent=2)

if __name__ == "__main__":
    main()
