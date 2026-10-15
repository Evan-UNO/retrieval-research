# Comparing papers around a question

Use when the user asks how papers relate, how they differ, or what to read next. Usually work with two to five papers and a specific comparison question; do not add papers just to reach a count.

## Inputs and comparison

- Reuse paper cards to locate materials, but revisit the original paper, supplement, or code for assumptions, mechanisms, or results that determine the conclusion. Summaries of summaries are not substitutes for decisive evidence.
- With titles alone, locate public abstracts and full texts where available. Leave unavailable fields unknown and explain the effect; do not infer losses or configurations from titles.
- Select dimensions relevant to the question: task and retrieval direction, supervision, where and how data are missing, continuous representations or hashes, optimization mechanism, data and evaluation protocol, and extra features or pretrained resources. Do not fill every dimension by default.
- Distinguish missing modalities, unpaired samples, missing labels, ambiguous candidate labels, and wrong labels. These are not one generic incomplete-data setting. Align each paper's definitions before comparing.

## Output and judgment

Answer the comparison question in one sentence, then provide a compact table. Attach source locations to important differences and explain their implications for applicability or interpretation. "Method A needs paired training examples" is more informative than "Method A is traditional."

Performance supports comparisons only within the scope justified by sufficiently aligned splits, relevance definitions, metric conventions, representations, and resources. Unknown conditions are not equal conditions. Explain what is missing when comparison is unsupported; read [protocol.md](protocol.md) for a detailed check. Complexity, recency, or higher author-reported numbers alone do not establish superiority.

For a reading recommendation or small experiment, identify the question suggested by the evidence, the concept or hypothesis to address, and which explanation the work could rule out. Distinguish author reports, current evidence, and hypotheses worth testing. Without experimental resources, provide a minimal plan without claiming validation.

## Completion criteria

The user should be able to explain whether the methods solve the same problem or adjacent problems, locate evidence for at least one difference, and identify conclusions not yet justified. Change comparison dimensions when supervision or representation changes; do not reuse conclusions from the previous papers.
