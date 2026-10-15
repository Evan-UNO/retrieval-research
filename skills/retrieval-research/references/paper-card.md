# Paper card: record only what was read and checked

Trim this outline to the question's depth. Omit inapplicable fields. Distinguish "not reported" from "not covered by the available material." Label an abstract-only introduction at the start and do not fill unseen method or experiment details.

## Identity and evidence coverage

- Title, authors, year, publication/preprint version, DOI or original link; Zotero item key when available.
- Files and sections read, the relationship between viewer and printed page numbers, unreadable figures, and missing pages.
- Place evidence near important claims, for example "PDF p. 4, Section 3.2, Eq. (5)." Use sections and stable links for unpaginated pages, or the supplied passage location for excerpts. Do not invent citation numbers or pages from memory.

## Problem, boundaries, and intuition

1. How does a concrete query enter the system, and what is returned? Identify modalities, query-to-pool direction, and representation.
2. Under which specific condition do existing methods struggle? What assumptions concern labels, pairing, pretrained features, missingness, or extra data?
3. Explain the method's intent with a brief example. Label a constructed teaching example rather than presenting it as an example from the paper.

## Method and equations

Explain inference as input -> key modules -> representation -> ranking, then explain how training obtains those modules. Add symbols, dimensions, loss terms, and optimized variables as needed. Explain how information available only during training is handled at inference.

Focus on equations central to the claims rather than copying every formula. Distinguish original equations, supplemental derivations, and intuitive analogies. Use a hand-calculable example when useful; it is not a paper experiment result.

## Experimental support and limits

| Claim | Source location and observation | Supported scope and remaining uncertainty |
|---|---|---|
| A claim actually read | Verifiable table, figure, or section observation | Explicit conditions and limits |

Record datasets and splits, directions, relevance definitions, metrics and cutoffs, representations and code lengths, supervision, or missingness only when visible in the source. Check experiments for one or two central claims. Separate author-discussed limitations from your own questions. Do not say "code-verified" or "successfully reproduced" without the corresponding inspection or run.

## Learning progress

- One to three concepts currently needed and how they relate to the method; add more only for a demonstrated learning obstacle.
- Two or three comprehension questions, initially without answers; record "awaiting self-check" or specific feedback based on actual answers.
- One feasible next action, such as hand-calculating a loss, checking one evaluation definition, or reading a related module. Do not automatically expand this into a large reading program.
