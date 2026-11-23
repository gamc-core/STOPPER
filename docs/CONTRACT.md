# Contract 0.1

**STOP REQUESTED IS NOT STOP EFFECTIVE.**

A worker cooperates by checking a request before it starts the next unit.
The receipt, the worker's outcome and a check of its actual effects answer
different questions.

## Execution and receipt

An execution is local to one process, with a fixed, finite, ordered list of
unique unit names. The caller assigns a distinct execution ID within its
routing context. STOPPER provides an object API rather than a global registry.

The worker calls `begin(unit)` before its operation, `complete(unit)`
after success, and `finish()` when done. Only one unit can be active.
When `begin` returns false, the worker must leave the loop. The library
does not create or terminate its worker thread.

Each execution has its own `threading.Event` and lock by default.
A custom `signal_factory` must supply a fresh independent adapter for
each execution. Its callbacks may read snapshots, but must not call methods
that change the execution; rejected reentry is a signal error.

A request names a request ID and target execution ID. A wrong target yields
`NOT_RECEIVED`. A correct request before terminal yields `RECEIVED`;
this confirms intake, not cooperation. Repeating its ID is idempotent.
A new request after terminal yields `TOO_LATE` without rewriting the outcome.

## Cooperation and completion

Under the execution lock, `begin` checks the signal before starting a unit.
If the signal is observed with units remaining, those units are prevented
and the job settles `STOPPED`. Its effect is `PREVENTED_FUTURE` when
no unit completed, or `INTERRUPTED` after partial work.

Both effects refer to abandoning the job at a unit boundary. The protocol
does not interrupt inside an active unit. Completed work remains in place.

`finish()` requires every unit completed unless the execution already
stopped or failed. A completed job with a preterminal request has effect
`NO_EFFECT`; ordinary completion without a request has effect `NONE`.
Signal read/write errors settle `FAILED` and raise `SignalError`.
A reported worker failure also settles `FAILED`, retaining its work counts.

## Seven invariants

| | Property | Boundary |
| --- | --- | --- |
| I1 | Receipt differs from effect. | `RECEIVED` does not imply `STOPPED`. |
| I2 | Requests belong to an execution. | Target mismatch cannot set its signal; default Events are separate. IDs are caller-chosen labels. |
| I3 | Prevention is not retroactive. | A started unit never appears in `prevented`; units begin in declared order. |
| I4 | Stopping does not undo work. | Completing a unit registers no rollback. |
| I5 | Incomplete work is not declared complete. | `COMPLETED` requires all units completed. A failed outcome does not confirm overall completion, even if all unit completions were reported. |
| I6 | A terminal outcome is stable. | Later requests cannot rewrite it. |
| I7 | An observation error is not a successful stop. | Signal failure yields `FAILED`; physical-check mismatch/error does not confirm the reported effect. |

## Outcome

An immutable snapshot records execution ID, state, effect, planned, started,
completed, not-started and prevented units, request IDs, observed checkpoints
and errors. The core does not persist files. A failed run can retain an
unfinished active unit whose physical effects still need inspection.

These counts are worker reports. The protocol enforces their order and state
transitions, but a worker can ignore it or report dishonestly. The examples
compare reports with actual files or data.

`observe_effects` expects a terminal outcome. Its supplied checker yields
`VERIFIED` only when it returns exactly true, `MISMATCH` when false,
and `ERROR` on an exception or non-boolean result. Agreement with that
checker is not independent certification or authentication.

## Limits

The scope excludes arbitrary process or subprocess-tree termination, remote
inference cancellation, automatic rollback, universal resume, guaranteed
latency, power-loss durability, distributed execution and hostile actors.

Examples place synthetic inputs and outputs under their checkout's `.runs/`.
The helpers accept paths throughout the checkout, use exclusive output creation,
and reject checked link/reparse paths. They do not provide containment against
concurrent hostile filesystem replacement.

[Working integration](../examples/05_independent_reuse/example.py) ·
[Coverage](VERIFICATION.md#contract-coverage) · [Main page](../README.md)
