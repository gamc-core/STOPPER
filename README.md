# STOPPER
*Cooperative stopping and observable outcomes*

**[Understand](#understand) → [Try](#try) → [Use](#use) → [Examine](#examine)**

## Understand

**You asked it to stop. What actually stopped?**

A copy operation receives your request while a file is still being written.
Other files are already complete. Before using the result, you need to know
what stopped and what remains.

STOPPER is a small Python library for cooperative stopping in operations you
control. Five executable experiences let you observe requests, worker responses
and partial results. You can try them without knowing the internals, or use
the same protocol in your own program.

## Try

Open a terminal in the STOPPER folder and run:

```text
python -I -S -B examples/run.py E02 --summary
```

E02 creates five synthetic files, copies two and stops before the remaining
three start. Its controller acts at a coordinated checkpoint; no manual
timing is needed.

Open `result.json` at the printed `Evidence` path. Beside it,
`source/` contains five files and `destination/` contains two.
[The E02 guide](examples/02_interrupt_copy/README.md) takes you through
comparing the report with the files and byte checks.

| Experience | What to examine |
| --- | --- |
| [E01 — Signal not received](examples/01_signal_not_received/README.md) | A misdirected request; both jobs complete. |
| [E02 — Interrupt a copy](examples/02_interrupt_copy/README.md) | Completed files and a partial destination. |
| [E03 — Stop without undoing](examples/03_stop_is_not_undo/README.md) | A change remains; the next phase is prevented. |
| [E04 — Withhold a result](examples/04_presentation_is_not_execution/README.md) | Work completes despite suppressed delivery. |
| [E05 — Use another operation](examples/05_independent_reuse/README.md) | Reuse in an arithmetic batch. |

Run all five with `python -I -S -B examples/run.py all --summary`.
Omit `--summary` for JSON console output. Saved `result.json` is
complete in either mode; each run creates new data under `.runs/`.

The commands require Python 3.10 or later, with no installation or download.
Use your interpreter's path if needed. The
[verified environment and limits](docs/VERIFICATION.md) are documented.

## Use

Add `src` to your Python module search path. Create an `Execution`
with a distinct ID and finite, ordered units. Call `begin(unit)` before
each operation and `complete(unit)` after success. Leave the loop when
`begin` returns false; `finish()` returns the outcome and `fail(...)`
reports a failure.

A controller holding the same object calls
`request_stop(request_id, execution_id)`.
[E05's working loop](examples/05_independent_reuse/example.py) can be adapted
to file processing, transformations or other batches with cooperation points.
The worker reports its work; `observe_effects` compares that report with
a supplied checker.

An AI-agent controller could check before each planned local step or tool call.
It must own the loop and define its units. No agent adapter is provided, and
a request does not cancel a model call or tool operation already in progress.

## Examine

[Historical experiences](docs/ORIGIN.md#historical-cases) →
[independent implementation](src/stopper/core.py) →
[executable examples](#try) →
[checked results](docs/VERIFICATION.md#observed-results).

These are reading paths, not runtime dependencies. Continue with the
[contract and seven invariants](docs/CONTRACT.md), [tests](tests/),
[decisions](docs/DECISIONS.md) or [origin](docs/ORIGIN.md).
Run the suite with `python -I -S -B tests/run.py`.

Cooperation happens between units. Completed work remains; STOPPER provides
neither process termination, automatic rollback nor a maximum stopping time.
It relies on a worker that follows the protocol.

Copyright 2026 Gonzalo Montero (GAMC). New code, prose and synthetic data use
[MIT](LICENSE). Private source records are not distributed or relicensed.
