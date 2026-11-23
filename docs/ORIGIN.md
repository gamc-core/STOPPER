# Origin

STOPPER grew from stop trials in Arquitectura Simbiótica, Gonzalo Montero (GAMC)'s environment for constructing and preserving work with human
involvement. DOJO provides its human interaction environment. In those trials,
a request to stop could reach a worker too late, prevent a later step, abandon
a copy, or change only what was delivered to the screen.

The historical mechanism developed from recording requests into cooperative
prevention, bounded copy interruption and more faithful feedback. STOPPER
takes those distinctions into a small independent implementation.

## Historical cases

| Experience | What remained important | New experiment |
| --- | --- | --- |
| [000129 — gesture not received](../cases/000129/README.md) | An attempted intervention did not reach intake. | [E01](../examples/01_signal_not_received/README.md) |
| [000132 — copy abandoned](../cases/000132/README.md) | An invalid partial remained; mutation never began. | [E02](../examples/02_interrupt_copy/README.md) |
| [000142 — change already made](../cases/000142/README.md) | Later validation stopped while the modification remained. | [E03](../examples/03_stop_is_not_undo/README.md) |
| [000144–147 — response withheld](../cases/000144_000147/README.md) | Local suppression did not demonstrate provider cancellation. | [E04](../examples/04_presentation_is_not_execution/README.md) |

These pages are new, sanitized summaries of checked historical records.
They separate the recorded facts and their limits from the interpretation
that motivated each example. The examples use synthetic inputs and produce
new results. STOPPER's tests concern its own code; historical test outcomes
do not transfer to it. E05 is a derived reuse example without another
historical episode.

## Independent construction

The execution API, receipts, outcome snapshots, observation helper, examples
and tests were implemented anew. Signaling uses Python's conventional
`threading.Event`. No private runtime or external library code was copied.

The construction retains the relationship between a request, its execution,
a cooperation boundary and the work left behind. It leaves out the original
execution and validation engines, authority contracts, promotion mechanisms,
private workspaces and source Git history.

Development began on 20 November 2026 with a new Git root, before code was
written. The implementation assistant was Codex, working under GAMC's
authorization. [Decisions](DECISIONS.md) records the real findings and
corrections. The 23 November reading revision preserves that history and
changes documentation only.

## Source record

The private inspection report
maps each case to its preserved conversation, request, settlement, intervention
and custody objects. It remains in the author's custody and is not needed
to use STOPPER.

The summaries omit personal paths, detailed execution IDs, full conversations,
work files and internal authority references. Session numbers remain as
historical locators. The inspection distinguished direct conversation fields,
transported human reports and consumer observations. It did not newly
authenticate people or establish a complete historical timeline; some
intermediate implementation versions were not preserved individually.

The underlying private records are not included. These summaries make their
relationship to the new experiments explicit without replacing the originals
or making the historical executions independently reproducible.

## Reuse

[MIT](../LICENSE) covers the new code, project prose and synthetic data.
It does not grant access to, or rights over, the underlying private records,
conversations or third-party material.

[Start with E02](../examples/02_interrupt_copy/README.md) ·
[Verification](VERIFICATION.md) · [Main page](../README.md)
