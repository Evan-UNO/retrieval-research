# Arithmetic checking script

`scripts/check_metrics.py` uses the Python 3 standard library for small constructed cases and ranking results with explicit protocols. It does not train models, determine splits, or recover undocumented author definitions.

```text
python scripts/check_metrics.py --self-test
python scripts/check_metrics.py --hamming 0101 1100
python scripts/check_metrics.py input.json
```

Use `-` as the path to read JSON from standard input. The script writes no files and prints JSON to standard output. Failures return a nonzero exit code with an error on standard error.

## Input contract

```json
{
  "k": null,
  "ap_denominator": "all_positives",
  "zero_positive": "exclude",
  "tie_break": "input_order",
  "queries": [
    {
      "query_id": "q1",
      "positive_ids": ["a", "c"],
      "candidates": [
        {"id": "a", "distance": 0},
        {"id": "b", "distance": 1},
        {"id": "c", "distance": 2}
      ]
    }
  ]
}
```

Provide every field explicitly. The candidate list must be the query's complete eligible candidate pool. Determine positives after self-match removal, deduplication, and other protocol filters; every positive ID must appear in the pool. Do not supply only top K while treating it as the full pool. The caller must verify completeness from source data; the script cannot infer omitted candidates.

- `distance` must be finite and nonnegative; smaller ranks first. Convert raw cosine similarities or other scores to distances under a checked convention. The script does not guess sort direction.
- `k: null` means the complete ranking. Otherwise K is a positive integer no larger than each query's candidate count. Every query needs at least one candidate. All IDs are nonempty strings; duplicate IDs within a collection are rejected.
- `ap_denominator: all_positives` uses the full-pool positive count R. `min_positives_k` uses min(R,K). They agree for a full ranking. Neither is an assumed default for an author's protocol.
- `zero_positive: exclude` excludes that query from every aggregate metric. `zero` assigns zero to all three metrics and includes the query in the means. `error` stops evaluation. If every query is excluded, aggregate values are `null`.
- `tie_break: input_order` preserves input order for equal distances. `id` breaks ties lexicographically by string ID, so `"10"` precedes `"2"`. The script does not compute expectations over random tie orders or average over ties; those author protocols need another check. Output identifies queries with distance ties.

The AP numerator is the sum of precision at each positive's position within the top K. `hit` is 1 if at least one positive appears in the top K, otherwise 0. `recall` is the number of positives retrieved in the top K divided by all positives in the pool. Do not label `mean_hit` or `mean_recall` as the authors' R@K without matching definitions first. `mean_ap` is the arithmetic mean of AP over included queries.

The Hamming command accepts only nonempty, equal-length 0/1 strings and counts differing positions. For -1/+1 codes, the caller must verify binary values and convert consistently. Thresholding real-valued hash outputs belongs to the original experiment protocol.

## Hand calculation and reuse limits

The example's full ranking has relevance `[1,0,1]`: AP = `(1 + 2/3) / 2 = 5/6`. At K=2, `all_positives` yields AP=1/2. With one positive at rank 2 and K=1, AP, hit, and recall are all zero.

Self-tests cover full/truncated AP, denominator differences, zero-positive policies, ties, duplicate/missing IDs, and invalid binary codes. New tasks still need cases derived from the actual evaluation implementation. Passing self-tests does not validate author code, full datasets, or training reproduction.
