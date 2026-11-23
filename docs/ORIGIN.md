# Origin

STOPPER is an independent construction by Gonzalo Montero (GAMC), informed by
problems observed while building and testing DOJO. DOJO is an environment
developed within Arquitectura Simbiótica (AS), the architecture behind that work.

Requests to stop could fail to reach their receiver, prevent a later step,
abandon a copy or change only what was delivered to the screen. Investigating
and recording those cases led to STOPPER's separate implementation.

## Historical cases

The numbers below identify DOJO session records. Each case retains the
examined facts, their limits and the interpretation behind its new example.

| Experience | Retained distinction | New example |
| --- | --- | --- |
| [000129 — gesture not received](../cases/000129/README.md) | An attempted stop did not reach intake. | [E01](../examples/01_signal_not_received/README.md) |
| [000132 — copy abandoned](../cases/000132/README.md) | An invalid partial remained; mutation never began. | [E02](../examples/02_interrupt_copy/README.md) |
| [000142 — change already made](../cases/000142/README.md) | Later validation stopped while the change remained. | [E03](../examples/03_stop_is_not_undo/README.md) |
| [000144–147 — response withheld](../cases/000144_000147/README.md) | Local suppression did not prove provider cancellation. | [E04](../examples/04_presentation_is_not_execution/README.md) |

The case pages are sanitized summaries, not original records or reproduced
historical executions. The examples use synthetic inputs and have their own
results and tests. E05 is a derived reuse example without a separate
historical episode.

## Independent construction

The API, receipts, outcome snapshots, observation helper, examples and tests
were implemented anew, using Python's conventional `threading.Event`.
No private runtime or external library code was copied. Authority contracts,
promotion mechanisms, private workspaces and source Git history were excluded.

Development began on 20 November 2026 with a new Git root, before code was
written. Codex assisted the implementation under GAMC's authorization.
[Decisions](DECISIONS.md) records the choices, failures and corrections;
[verification](VERIFICATION.md) identifies the tested revisions.
Historical tests do not validate the new code.

## Source record

The author retains private records linking the cases to the original
conversations and observations. They remain under private custody and are
unnecessary for running STOPPER.

The inspection distinguished conversation fields, transported human accounts
and consumer observations. It did not authenticate people or establish a
complete historical timeline; some intermediate source versions were not
retained. Private records, full conversations and work files are not included.

[MIT](../LICENSE) covers the new code, project prose and synthetic data,
not the underlying private records or third-party material.

[Try E02](../examples/02_interrupt_copy/README.md) · [Main page](../README.md)
