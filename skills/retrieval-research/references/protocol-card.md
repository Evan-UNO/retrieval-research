# Protocol card

Choose fields for the task. Distinguish "not applicable" from "unknown/not disclosed." For multiple papers, split the content column by paper and retain a source for every item.

| Core field | Content | Source or location to check |
|---|---|---|
| Paper/experiment identity | Title, version, repository commit, target table entry | |
| Retrieval direction | Image-to-text, text-to-image, separately reported or not | |
| Data and splits | Data version; train/validation/query/candidate counts and IDs; overlap | |
| Candidate organization | Multiple captions per image, duplicates, filters, self-match removal | |
| Relevance | Same instance, at least one shared label, graded relevance, or another explicit rule | |
| Representation and ranking | Continuous vector/binary code; distance or similarity; sort order; normalization; tie handling | |
| Metric definition | Source formula/code; full pool or K; AP denominator; zero-positive policy | |
| Aggregation | Per-query averaging, weighting, direction averaging, repeated runs and variance | |
| Resources and supervision | Features, pretrained model/weights, frozen or fine-tuned, labels, extra training data | |
| Number provenance | Author report, secondary citation, or local measurement; units/percentages; configuration | |

Check the definition of R@K. Some image-text implementations measure the fraction of queries with any correct match in the top K; multi-positive retrieval may instead use retrieved positives divided by all positives. The name does not determine the formula, and these definitions are not interchangeable.

## Additional fields for hashing

Code length; binarization of real outputs including zero handling; 0/1 versus -1/+1 encoding; Hamming ranking versus radius retrieval; radius and empty-return policy; tie order among equal-distance candidates; exhaustive pool versus approximate index; whether retrieval cost includes encoding and indexing.

Different code lengths can form an accuracy/storage curve, but do not show superiority at the same code length. Before converting a -1/+1 inner product to Hamming distance, verify that every value is binary. Unthresholded real vectors do not satisfy the equivalence.

## Additional fields for missing modalities

Whether missingness occurs in training, queries, or the candidate pool; affected modalities; sample pairing; complete-pair count; missing-rate denominator; random or sample-dependent missingness; shared seeds and masks; access at test time to supposedly missing modalities; imputation and the information available to it.

"50% missing" may mean a fraction of samples, modality entries, or unpaired samples. Inspect generation code or the source definition. Do not equate incomplete, unpaired, and missing-modality settings without evidence.

## Additional fields for incomplete label supervision

Label semantics: multi-label targets, candidate sets, observed labels, and true labels. How ambiguity, missingness, or errors are generated and at what rates. Labels accessible during training. Whether evaluation relevance uses true or observed labels. Possible true-label leakage in validation or tuning.

Interpret partial, missing, and noisy labels through each paper's definitions, not wording alone: distractors in a candidate set, unobserved true labels, or incorrect annotations are distinct. Follow and identify any different definition used by the paper.

## Comparison conclusion

- **Claim being compared:** Accuracy under the same protocol, robustness, storage/compute cost, or another specific objective.
- **Conclusion and limits:** Directly comparable, comparable under stated conditions, not directly comparable, or unresolved.
- **Evidence:** Decisive fields and sources.
- **Impact of differences:** How they affect ranking, relevance, available information, or resources.
- **Smallest addition:** One field to locate or condition to rerun, without unrelated large experiments.
