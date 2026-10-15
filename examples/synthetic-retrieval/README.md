# Synthetic retrieval example

This is a small, fully synthetic exercise for running and explaining a retrieval evaluation. It is not a real dataset, a trained model, or a reproduction of a paper. It uses Python 3 and the standard library only: no installation, downloads, GPU, or Zotero access is needed.

## Run from the repository root

```sh
python examples/synthetic-retrieval/baseline.py --model A --evaluator skills/retrieval-research/scripts/check_metrics.py --output-dir runs/A
python examples/synthetic-retrieval/baseline.py --model B --evaluator skills/retrieval-research/scripts/check_metrics.py --output-dir runs/B
```

Each command prints its result as JSON and saves `evaluation-input.json` and `results.json` in its output directory. A second run using the same output directory overwrites these files. The result includes ranked candidate IDs, per-query AP, and group means.

To exercise the failure path, first ensure that `missing-inputs.json` does not exist in the repository root, then run:

```sh
python examples/synthetic-retrieval/baseline.py --inputs missing-inputs.json --model A --evaluator skills/retrieval-research/scripts/check_metrics.py --output-dir runs/missing-input
```

This deliberately missing input should produce an error on standard error and exit code `2`, without creating results for that run. It is an input failure, not evidence that a retrieval model failed. Keep actual commands, exit codes, standard output, and standard error in your own run records.

## What is being evaluated?

The artificial task is a multimodal query bundle retrieving text candidates. Four query IDs each have the same four candidate IDs, with explicitly assigned positive IDs. A and B are labels for preset distances, not learned models. Lower distance ranks first; equal distances are ordered by candidate ID.

Evaluation uses the full candidate list (`k: null`). Average precision (AP) sums precision at each positive rank and divides by the total number of positives for that query. Mean AP (mAP) is the unweighted mean across included queries. Queries with no positives would be excluded; this example has none. The labels `complete`, `missing_text`, and `missing_image` describe synthetic groups only: there is no actual image, text, masking process, or missing-modality mechanism.

## Hand-checkable reference values

| Query | Group | Positive IDs | AP for A | AP for B |
|---|---|---|---:|---:|
| q1 | complete | c1, c3 | 5/6 | 1 |
| q2 | complete | c2 | 1 | 1/2 |
| q3 | missing_text | c4 | 1/4 | 1 |
| q4 | missing_image | c2, c4 | 1/2 | 1 |

For example, A ranks q1's positives at positions 1 and 3, so its AP is `(1 + 2/3) / 2 = 5/6`.

| Group | Query count | Mean AP for A | Mean AP for B |
|---|---:|---:|---:|
| complete | 2 | 11/12 | 3/4 |
| missing_text | 1 | 1/4 | 1 |
| missing_image | 1 | 1/2 | 1 |
| All queries | 4 | **31/48 = 0.645833...** | **7/8 = 0.875** |

B improves three queries and worsens one. Its overall mAP rises by `11/48`, while the complete group's mean AP falls by `1/6`. The two other groups contain only one query each, so these numbers cannot establish general missing-modality robustness. Full-list hit and recall are both `1` for A and B; neither is Recall@1.

## Use with the skill

Give an assistant [task.txt](task.txt) and this directory while using the `retrieval-research` skill. The task asks it to run the example, explain per-query and grouped results, design a discriminating small experiment, state the limits of semantic explanations, and prepare a three-minute lab-meeting outline from actual execution evidence.

For a blind workflow check, withhold this README's reference-value section until the assistant has produced its answer. The skill should distinguish a working synthetic ranking/evaluation pipeline from model training or a successful paper reproduction.
