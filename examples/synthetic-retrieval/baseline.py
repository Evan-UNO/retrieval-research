#!/usr/bin/env python3
"""Synthetic ranking fixture, not training or a paper reproduction; stdlib only."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("inputs.json"))
    parser.add_argument("--model", required=True, choices=("A", "B"))
    parser.add_argument("--evaluator", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        source = json.loads(args.inputs.read_text(encoding="utf-8-sig"))
        if source.get("synthetic") is not True:
            raise ValueError("This fixture accepts only explicitly synthetic inputs")
        inputs = {**source["protocol"], "queries": []}
        groups = {}
        for query in source["queries"]:
            candidates = query["candidate_ids"]
            distances = query["distances"][args.model]
            if len(candidates) != len(distances):
                raise ValueError(f"{query['query_id']}: candidate/distance lengths differ")
            inputs["queries"].append({
                "query_id": query["query_id"], "positive_ids": query["positive_ids"],
                "candidates": [{"id": item, "distance": distance}
                               for item, distance in zip(candidates, distances)],
            })
            groups[query["query_id"]] = query["group"]
        args.output_dir.mkdir(parents=True, exist_ok=True)
        evaluation_path = args.output_dir / "evaluation-input.json"
        evaluation_path.write_text(json.dumps(inputs, indent=2), encoding="utf-8")
        run = subprocess.run([sys.executable, str(args.evaluator), str(evaluation_path)],
                             capture_output=True, text=True, encoding="utf-8", check=True)
        result = json.loads(run.stdout)
        for row in result["per_query"]:
            row["group"] = groups[row["query_id"]]
        result.update(synthetic=True, model=args.model, execution="fixed-distance-ranking-only")
        result["group_mean_ap"] = {}
        for group in sorted(set(groups.values())):
            values = [row["ap"] for row in result["per_query"]
                      if row["group"] == group and row["status"] == "included"]
            result["group_mean_ap"][group] = sum(values) / len(values) if values else None
        text = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
        (args.output_dir / "results.json").write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    except subprocess.CalledProcessError as error:
        print(f"evaluator failed: {error.stderr.strip()}", file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
