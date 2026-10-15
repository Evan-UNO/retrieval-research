# Minimal baseline reproduction

Turn one paper result into an experiment supported by actual execution. Start with a result the user cares about, then expand the run scope only as needed.

## Define the target

Determine from available materials: paper version and target table entry, repository commit, data or feature version, pretrained weights, retrieval direction and metric, available machine, and time budget. For hashing, record code length. For missing modalities, record the definition, mask generation, and where masks apply across training, queries, and candidates. Do not ask again for information available in the configuration or environment.

For a broad reproduction request, select one dataset and the smallest executable path, explaining the choice. Keep consequential missing conditions unknown. Check code, data entry points, and evaluation scripts while waiting for missing resources rather than stopping all work.

## Execution

1. Read project instructions, entry points, and dependencies; establish the expected data structure. Check actual splits, sample IDs, feature sources, and label semantics. Do not confuse training or candidate data with queries. Route paper/code protocol discrepancies to this skill's protocol workflow.
2. Prefer inference with available weights or an existing quick example. Otherwise use a small, clearly labeled test input to exercise loading, forward computation, loss, and evaluation. Synthetic input checks the pipeline, not paper performance.
3. Check output shapes, finite values, sample counts, query/candidate alignment, and metric conventions. Once the pipeline works, run the target within the authorized machine and budget. Do not independently rent a cloud GPU, pay for resources, or expand to long full-scale training. With an unknown budget, start with code inspection and lightweight pipeline checks.
4. Record actual dependencies or environment files, working directory, commands, configuration, seeds, splits and masks, data/weight sources, run scope, exit status, and log/result locations. Reuse sufficient environment files rather than adding another environment management system. Distinguish executed commands from prepared but unexecuted commands.
5. Compare with the paper target, reporting absolute differences and known condition mismatches. A single mismatch does not establish a code bug or randomness as its cause. Do not declare success "within error" when no tolerance or repeated-run evidence supports that judgment.

When blocked, identify the resource gap, such as missing weights, unknown data version, or insufficient memory. Continue feasible static tracing, protocol checks, and runnable configuration preparation. State the smallest input needed to unblock execution; preparation is not a successful run.

## Record and status

A compact record is enough: `target/version | actual resources/scope | commands/configuration | actual results | difference from paper | unresolved conditions | next step`. Preserve logs for reruns without imposing a new directory or input format.

Choose status from evidence; subtasks may have different statuses:

- **Plan prepared:** Target and commands identified, not yet executed.
- **Pipeline runs:** Loading, inference or training steps, and evaluation executed; identify synthetic, subset, or complete data.
- **Small-scale validation:** Results obtained on a real subset or reduced setting; do not extrapolate to the full experiment.
- **Target experiment executed, original result not yet reproduced:** The run completed, but settings differ, discrepancies remain unexplained, or judgment criteria are missing.
- **Original result reproduced:** Target settings and protocol checked, and actual results satisfy a previously agreed evaluation criterion. State the covered results and remaining differences; one reproduced row does not establish reproduction of the whole paper.

Validate reuse by rerunning from the record in a fresh directory or changing a configuration-controlled condition. Explain changes that require implementation work; do not promise every method can be adapted through configuration alone.
