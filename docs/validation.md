# Validation scope

The prepublication v2 skill was exercised in independent assistant contexts on a comparison of real retrieval papers and on the synthetic pipeline now provided under [`examples/synthetic-retrieval`](../examples/synthetic-retrieval/). Those task-level checks examined whether answers used available evidence, respected comparison limits, executed the requested small workflow, and separated observed results from unverified claims. Private reading materials and local execution logs are not distributed here.

The public English guidance is a translation of that v2 package. Both bundled Python scripts are unchanged byte for byte. The earlier task-level checks do not constitute a fresh independent validation of every translated instruction.

Public-package checks cover the required skill files and local references, Python syntax, the metric evaluator's built-in self-test, and fresh A/B executions using the example and the evaluator in this repository. The deliberately missing-input case was also executed to verify a nonzero failure with no result. The example's per-query AP and aggregate values match its hand calculations: A has mAP `31/48`, B has `7/8`, and the complete group decreases from `11/12` to `3/4` over two queries.

These checks validate packaging and a small synthetic ranking/evaluation workflow. No real GPU training, full-dataset benchmark reproduction, semantic-error validation, or real-paper performance claim is established by them. The synthetic groups do not implement a real missing-modality mechanism.
