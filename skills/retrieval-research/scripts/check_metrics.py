#!/usr/bin/env python3
"""Small retrieval-metric checks with explicit policies; Python standard library only."""

import argparse
import copy
import json
import math
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def hamming(left, right):
    require(bool(left) and len(left) == len(right), "codes must be nonempty and equal length")
    require(set(left + right) <= {"0", "1"}, "codes must contain only 0 and 1")
    return sum(a != b for a, b in zip(left, right))


def unique_ids(values, label):
    require(isinstance(values, list), f"{label} must be a list")
    require(all(isinstance(x, str) and x for x in values), f"{label} requires nonempty string IDs")
    require(len(set(values)) == len(values), f"{label} contains duplicate IDs")


def evaluate(data):
    require(isinstance(data, dict), "input must be an object")
    k = data["k"]
    require(k is None or (type(k) is int and k > 0), "k must be null or a positive integer")
    denominator = data["ap_denominator"]
    zero_policy = data["zero_positive"]
    tie_policy = data["tie_break"]
    require(denominator in ("all_positives", "min_positives_k"), "unknown ap_denominator")
    require(zero_policy in ("exclude", "zero", "error"), "unknown zero_positive policy")
    require(tie_policy in ("input_order", "id"), "unknown tie_break policy")
    queries = data["queries"]
    require(isinstance(queries, list) and queries, "queries must be a nonempty list")
    require(all(isinstance(q, dict) for q in queries), "each query must be an object")
    unique_ids([q["query_id"] for q in queries], "query_id")
    rows = []
    for query in queries:
        query_id = query["query_id"]
        positives = query["positive_ids"]
        unique_ids(positives, f"{query_id}: positive_ids")
        candidates = query["candidates"]
        require(isinstance(candidates, list) and candidates, f"{query_id}: candidates must be nonempty")
        require(all(isinstance(c, dict) for c in candidates), f"{query_id}: each candidate must be an object")
        ids = [c["id"] for c in candidates]
        unique_ids(ids, f"{query_id}: candidate IDs")
        require(set(positives) <= set(ids), f"{query_id}: positive ID missing from candidate universe")
        distances = [c["distance"] for c in candidates]
        require(all(type(d) in (int, float) and math.isfinite(d) and d >= 0 for d in distances),
                f"{query_id}: distances must be finite nonnegative numbers")
        limit = len(candidates) if k is None else k
        require(limit <= len(candidates), f"{query_id}: k exceeds candidate count")
        key = (lambda c: (c["distance"], c["id"])) if tie_policy == "id" else (lambda c: c["distance"])
        ranking = sorted(candidates, key=key)[:limit]
        row = {"query_id": query_id, "k_used": limit, "positive_count": len(positives),
               "has_ties": len(set(distances)) < len(distances),
               "ranked_ids": [c["id"] for c in ranking]}
        if not positives:
            require(zero_policy != "error", f"{query_id}: query has no positives")
            row.update(status="excluded" if zero_policy == "exclude" else "included",
                       ap=None if zero_policy == "exclude" else 0.0,
                       hit=None if zero_policy == "exclude" else 0.0,
                       recall=None if zero_policy == "exclude" else 0.0)
        else:
            positive_set = set(positives)
            hits = 0
            precision_sum = 0.0
            for rank, candidate in enumerate(ranking, 1):
                if candidate["id"] in positive_set:
                    hits += 1
                    precision_sum += hits / rank
            divisor = len(positives) if denominator == "all_positives" else min(len(positives), limit)
            row.update(status="included", ap=precision_sum / divisor,
                       hit=float(hits > 0), recall=hits / len(positives))
        rows.append(row)
    included = [r for r in rows if r["status"] == "included"]
    result = {"policies": {key: data[key] for key in ("k", "ap_denominator", "zero_positive", "tie_break")},
              "query_count": len(rows), "included_count": len(included),
              "excluded_count": len(rows) - len(included), "per_query": rows}
    for metric in ("ap", "hit", "recall"):
        result[f"mean_{metric}"] = (sum(r[metric] for r in included) / len(included)) if included else None
    return result


def self_test():
    sample = {"k": None, "ap_denominator": "all_positives", "zero_positive": "exclude",
              "tie_break": "input_order", "queries": [{"query_id": "q1", "positive_ids": ["a", "c"],
              "candidates": [{"id": "a", "distance": 0}, {"id": "b", "distance": 1},
                             {"id": "c", "distance": 2}]}]}

    def changed(**changes):
        item = copy.deepcopy(sample)
        item.update(changes)
        return item

    def fails(item):
        try:
            evaluate(item)
        except ValueError:
            return
        raise AssertionError("invalid input was accepted")

    result = evaluate(sample)
    assert math.isclose(result["mean_ap"], 5 / 6)
    assert result["mean_recall"] == result["mean_hit"] == 1
    assert evaluate(changed(k=1))["mean_ap"] == 0.5
    assert evaluate(changed(k=1, ap_denominator="min_positives_k"))["mean_ap"] == 1
    assert evaluate(changed(k=2))["mean_ap"] == 0.5
    assert hamming("0101", "1100") == 2

    ties = changed(k=1)
    ties["queries"][0]["candidates"] = [{"id": "b", "distance": 0}, {"id": "a", "distance": 0},
                                        {"id": "c", "distance": 1}]
    assert evaluate(ties)["mean_hit"] == 0
    ties["tie_break"] = "id"
    assert evaluate(ties)["mean_hit"] == 1
    assert evaluate(ties)["per_query"][0]["has_ties"]

    empty = changed()
    empty["queries"][0]["positive_ids"] = []
    assert evaluate(empty)["mean_ap"] is None
    empty["zero_positive"] = "zero"
    assert evaluate(empty)["mean_ap"] == 0
    empty["zero_positive"] = "error"
    fails(empty)
    mixed = changed()
    mixed["queries"].append({"query_id": "empty", "positive_ids": [],
                             "candidates": [{"id": "a", "distance": 0}]})
    assert evaluate(mixed)["excluded_count"] == 1
    assert math.isclose(evaluate(mixed)["mean_ap"], 5 / 6)
    mixed["zero_positive"] = "zero"
    assert math.isclose(evaluate(mixed)["mean_ap"], 5 / 12)

    for field, value in (("positive_ids", ["x"]), ("positive_ids", ["a", "a"]),
                         ("candidates", [{"id": "a", "distance": 0}, {"id": "a", "distance": 1}]),
                         ("candidates", [{"id": "a", "distance": float("nan")},
                                         {"id": "c", "distance": 1}])):
        invalid = changed()
        invalid["queries"][0][field] = value
        fails(invalid)
    fails(changed(k=4))
    fails(changed(k=True))
    for left, right in (("", ""), ("0", "11"), ("0x", "01")):
        try:
            hamming(left, right)
        except ValueError:
            continue
        raise AssertionError("invalid binary code was accepted")
    return {"self_test": "passed", "checks": "AP, cutoff denominators, zero positives, ties, ID integrity, Hamming"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON input path, or - for stdin")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--hamming", nargs=2, metavar=("LEFT", "RIGHT"))
    args = parser.parse_args()
    if args.input and (args.self_test or args.hamming):
        parser.error("input cannot be combined with --self-test or --hamming")
    try:
        if args.self_test:
            result = self_test()
        elif args.hamming:
            result = {"hamming_distance": hamming(*args.hamming)}
        elif args.input:
            raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8-sig")
            result = evaluate(json.loads(raw))
        else:
            parser.error("provide an input path, --self-test, or --hamming")
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
