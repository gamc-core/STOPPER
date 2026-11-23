# STOPPER
*Cooperative stopping and observable outcomes*

**[Understand](#understand) → [Try](#try) → [Use](#use) → [Examine](#examine)**

## Understand

**You asked it to stop. What actually stopped?**

You ask a copy operation to stop. A file may still be writing; others may
already be complete. Before using the result, you need to know what stopped
and what remains.

STOPPER is a small Python library for adding cooperative stopping to operations
you control. Five executable experiences show what happens when a request
arrives, what work remains and how the result can be checked.

Try the experiences to observe the behavior, or use the library in your own
Python program. No knowledge of its source environment is needed.

## Try

Open a terminal in the repository root:

```text
python -I -S -B examples/run.py E02
```

The example creates five small files, copies two and stops before the other
three begin. Its controller requests stop at a coordinated point; no manual
timing is needed.

The printed `evidence_directory` is relative to the repository root.
Open it: `source/` holds five files, `destination/` holds two, and
`result.json` records completed and prevented work.
[Follow E02 step by step](examples/02_interrupt_copy/README.md) to compare
the report with the files and byte checks.

Python 3.10 or later is required; use your interpreter's path if needed.
These commands need no installation or download. Source execution was tested
on Windows 10 with CPython 3.10.6.

| Experience | What you can examine |
| --- | --- |
| [E01 — Signal not received](examples/01_signal_not_received/README.md) | Wrong delivery; both jobs complete. |
| [E02 — Interrupt a copy](examples/02_interrupt_copy/README.md) | Completed files and a partial destination. |
| [E03 — Stop without undoing](examples/03_stop_is_not_undo/README.md) | A change remains; the next phase is prevented. |
| [E04 — Withhold a result](examples/04_presentation_is_not_execution/README.md) | Work completes although delivery is suppressed. |
| [E05 — Use another operation](examples/05_independent_reuse/README.md) | Reuse in a separate arithmetic batch. |

Run all five with `python -I -S -B examples/run.py all`.
Each run saves new synthetic data under `.runs/`.

## Use

Add `src` to your Python module search path. Give an `Execution` a
distinct ID and ordered units. Call `begin(unit)` before each operation,
`complete(unit)` after success, and leave the loop when `begin` returns
false. `finish()` returns the outcome; `fail(...)` reports a failure.

A controller holding the same object calls
`request_stop(request_id, execution_id)`.
[E05's working loop](examples/05_independent_reuse/example.py) shows the
integration. The worker supplies its report; `observe_effects` compares
it with a supplied checker, distinguishing agreement, mismatch and errors.

## Examine

[Historical experiences](docs/ORIGIN.md#historical-cases) →
[independent implementation](src/stopper/core.py) →
[executable examples](#try) →
[checked results](docs/VERIFICATION.md#observed-results).

These arrows describe relationships, not runtime dependencies.
The examples run without the historical records. Continue through the
[contract and invariants](docs/CONTRACT.md), [tests](tests/),
[development decisions](docs/DECISIONS.md) or [origin](docs/ORIGIN.md).
Run the suite with `python -I -S -B tests/run.py`.

### Scope and license

Cooperation happens between units; an active unit may finish after a request.
Completed work remains. STOPPER does not kill processes, cancel remote
inference, provide general rollback or promise a stopping time.
It relies on a worker that follows the protocol.

[Verification](docs/VERIFICATION.md) identifies tested versions and remaining
limits, including unverified package installation and other platforms.

Copyright 2026 Gonzalo Montero (GAMC). New code, project prose and synthetic
data are under [MIT](LICENSE). Private source records are not distributed
or relicensed.
