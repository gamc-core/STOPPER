# Contract 0.1

STOP REQUESTED IS NOT STOP EFFECTIVE.

## Scope
One in-process execution has a fixed, finite, ordered list of unique unit names.
Its worker calls `begin(unit)` before each unit, `complete(unit)` afterward,
and `finish()` when done. The library owns a fresh threading.Event and lock by default. A custom
signal_factory must return an independent adapter for each execution.
A worker must stop calling its operation when begin returns false.
Only one unit may be active; the library does not create or terminate threads.

A request contains a request ID and target execution ID.
A wrong target is NOT_RECEIVED by this execution. A correct preterminal request
is RECEIVED; this proves intake, not worker cooperation. Repeating its ID is
idempotent. A new request after terminal is TOO_LATE and cannot rewrite outcome.

begin checks the signal before starting a unit, under the execution lock.
If observed with units remaining, it prevents those units and settles STOPPED.
A partial run has effect INTERRUPTED; a stop before any unit has effect
PREVENTED_FUTURE. These mean cooperative abandonment at a unit boundary.
An active unit cannot be interrupted. finish requires all units completed
unless an earlier boundary already settled STOPPED or the worker failed.
A request with no remaining work has effect NO_EFFECT; otherwise a normal
completion has effect NONE. Signal read/write errors settle FAILED and raise
SignalError. Worker failure settles FAILED, retaining started/completed work.

## Invariants and their boundaries
- I1: RECEIVED does not imply STOPPED; receipt and outcome are separate.
- I2: target mismatch cannot set this execution's signal; instances do not share
  their default Event. IDs are caller-chosen labels, not authenticated actors.
- I3: started units never appear in prevented. Units run in declared order.
- I4: no rollback; completing a unit does not register an undo operation.
- I5: COMPLETED requires every planned unit completed; STOPPED/FAILED is partial.
- I6: terminal outcome is stable under later requests, including late requests.
- I7: signal failure is FAILED, never a successful stop. Physical observation
  produces VERIFIED, MISMATCH or ERROR separately. Neither MISMATCH nor ERROR
  confirms a reported effect.

The library enforces this protocol, not the truthfulness of arbitrary workers.
Started/completed are worker reports. The examples compare reports with their
actual files/data. A worker can lie or ignore begin; STOPPER cannot prevent that.
observe_effects catches observation errors; VERIFIED means only that the
supplied local checker returned exactly True. It is not an independent
certificate, authentication, or proof of complete system history.

## Outcome
An immutable snapshot records execution ID, terminal state, effect, planned,
started, completed, not_started, prevented, request IDs, observed checkpoints,
and error information. No file persistence is required by the core.
A FAILED run may retain an active/incomplete unit: its effects are unknown
until the caller inspects them. No incomplete outcome is called COMPLETED.

## Exclusions
No arbitrary process kill, remote inference cancellation, subprocess-tree
termination, rollback, universal resume, maximum latency, crash durability,
authentication, distributed execution, or hostile-process containment.

Examples write only synthetic data under their own repository's .runs directory.
They reject preexisting outputs and reparse/link paths where checked. Concurrent
hostile filesystem replacement is outside the trust model.
