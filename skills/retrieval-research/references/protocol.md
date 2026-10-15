# Checking retrieval evaluation protocols

Help a new graduate student understand how a number was obtained and which results can be compared. Follow the user's language and briefly explain new terminology. Address the specific metric or comparison question first.

## Inputs and evidence

Accept any available full paper or experiment section, evaluation code, configuration, split information, or per-query results. Inspect available materials without requiring a complete package. Titles and abstracts locate papers; they do not establish splits, metric formulas, or actual training results. Finish supported checks before identifying the smallest missing input.

Record paper version and page/section/equation/table, code version and file/function/line, and executed commands with actual output. Separate paper specification, code behavior, actual measurements, and unresolved points. Show conflicting paper/code evidence side by side and explain its impact rather than silently choosing one. Static code analysis is not a passed runtime test. Claim current Zotero access only after a successful read; identify a snapshot's source and time.

## Checks by task

- **Protocol or result comparison:** Read the [protocol card and conditional fields](protocol-card.md). Fill relevant fields and use hash, missing-modality, or label-supervision branches only when applicable. Continuous-vector retrieval does not need hash-specific fields.
- **Formula or evaluation code:** Trace query/candidate IDs, relevance construction, sorting, cutoff, per-query aggregation, and final averaging. Check a few hand-calculable inputs. Read the [script conventions and input](metric-check.md) before arithmetic checks. `scripts/check_metrics.py` implements only its documented conventions; verify other definitions separately under the original protocol rather than overriding the authors' definition.
- **Aggregate table only:** Check disclosed conditions and state comparison limits. Without per-query results, do not infer error groups, significance, or implementation correctness.

Classify comparisons as supported directly, supported only under stated limits, not directly comparable, or unresolved because essential information is missing. Different splits, relevance rules, candidate pools, retrieval directions, or metric conventions prevent ranking models by the numbers alone. Different pretrained models, supervision, extra data, code lengths, or compute budgets require an explicit comparison objective and limits; separate accuracy and cost when useful.

## Delivery

Provide a short conclusion, a sourced protocol card or difference table, confirmed issues, and the smallest useful next step. Retain unknown fields rather than filling the template speculatively. For executed checks, include inputs, commands, actual results, and coverage. Passing a toy case establishes agreement only for that case, not successful reproduction.

Save reusable configurations, cards, or check outputs where requested; otherwise prefer chat. Input papers and run results remain separate artifacts, not fixed rules inside the skill.
