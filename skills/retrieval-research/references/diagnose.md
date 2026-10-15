# Failure analysis and the next experiment

Explain observable differences in existing retrieval results and turn possible causes into small experiments. Accept existing CSV, JSON, arrays, logs, or code outputs. Adapt to their format rather than requiring another data platform.

## Establish whether analysis is valid

- Read query IDs, candidate IDs, per-query rankings or scores, positive definitions, configurations, and protocols. Check ID uniqueness, coverage, alignment, candidate sets, duplicates, missing records, and sort direction. Align by ID, not assumed file row order.
- For model comparison, verify the same queries, candidate pool, positives, cutoff, and metric conventions. State mismatches first. If recomputing under common conditions is possible, explain filtering effects and preserve the chosen subset; do not silently drop samples and describe the result as a full comparison.
- With only aggregate mAP or similar numbers, analyze disclosed conditions and values, then identify the smallest steps to obtain per-query results. Do not infer specific failures, group effects, or statistical significance.

Before recalculating metrics, read the [script conventions](metric-check.md). Use `scripts/check_metrics.py` or repository evaluation logic under the actual definition. Different conventions prevent substituting the helper directly for the original implementation.

## Turn differences into hypotheses

1. Calculate per-query changes and check that aggregate metrics can be reconstructed. Count improvements, regressions, and ties. Include representative changes and common failures; showing only the largest regressions overstates typical behavior.
2. Group only by available, supported labels, such as retrieval direction, actual missingness pattern, class, or query length. Report group sizes and metrics. Do not generalize extreme values in small groups to the whole dataset; identify overlapping groups in multi-label analysis.
3. When raw images, text, or videos are available, inspect queries, positives, and misranked candidates, including whether annotations cover plausible visible matches. Without raw samples, describe ranking or label differences only; do not invent semantic explanations such as ignoring color or misunderstanding actions.
4. For each main candidate explanation, propose a falsifiable small experiment: what changes, what is controlled, what is observed, and what would weaken the hypothesis. Check ID, protocol, data, and run errors before new modules or large training. Correlation and a few visualizations do not prove causality.

A compact record can be:

| Observation and source | Candidate explanation | Minimal test | Results that support or weaken it |
|---|---|---|---|
| Actual result with query IDs or group scope | Explicit hypothesis | Variable, controls, and budget | Judgment rule stated before running |

## Delivery and reuse

Present confirmed differences, then unverified explanations and one prioritized experiment. Cases include query/candidate IDs, source files, and rank changes for manual checking. If estimating uncertainty, state the sampling unit and method. Without pairable records or defensible assumptions, do not claim significance.

The analysis should work on another model's results, identify concrete ID mismatches in deliberately misaligned input, and narrow to verifiable statistics when samples are unavailable. Consistent formatting is not the acceptance test; detecting invalid input and respecting evidence limits are.
