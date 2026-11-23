# Verification

The current presentation revision passed **53 tests in the original checkout
and an independent Git copy**: 34 existing checks plus 19 presentation tests.
All five scenarios ran in JSON and summary modes. Saved results were
byte-identical between modes and to the original baseline.

Tested executable revision: `b3ff3eb849074fc97ca1f3a733ea9a9607e6bc48`.
Subsequent documentation changes leave the Python files unchanged.
The attribution correction changes the project author metadata only.

## Reproduce

From the STOPPER folder, using your Python interpreter:

```text
python -I -S -B tests/run.py
python -I -S -B examples/run.py all --summary
```

For a first experience, use `E02` instead of `all` and follow
[the copy guide](../examples/02_interrupt_copy/README.md).
The `Evidence` line points to the complete saved `result.json`.
Omit `--summary` for JSON console output, including `evidence_directory`.

The verified environment is Windows 10, build 19045, CPython 3.10.6, 64-bit.
Runtime dependencies are standard-library-only. Package installation, wheel
building, other platforms/interpreters and third-party reproduction remain
unverified.

## Observed results

| Scenario | Result |
| --- | --- |
| E01 | `NOT_RECEIVED`; both jobs completed without observing a stop signal. |
| E02 | `STOPPED / INTERRUPTED`; two files copied, three not started; copied bytes and unchanged source hashes checked. |
| E03 | The modification remained; the validation marker was absent. |
| E04 | `COMPLETED / NO_EFFECT`; the result existed while delivery was withheld. A later `TOO_LATE` request did not rewrite the outcome. |
| E05 | The ordinary batch produced five values; the stopped run retained two and prevented three. |

The copy control uses the same worker without a request and completes all five
files. E05 also has an ordinary control. Explicit checkpoints establish request
order; the ten-second waits detect broken coordination rather than set stop
timing. File-example teardown checks that no named example worker remains alive.

## Contract coverage

| Invariant | Evidence |
| --- | --- |
| I1 — Request differs from effect | Receipt before cooperation; E01 and E04. |
| I2 — Execution identity | Wrong target, separate default Events, fixed identity and distinct E05 IDs. |
| I3 — No retroactive prevention | Active-unit request; disjoint started/prevented sets. |
| I4 — No implicit rollback | Retained modification in E03 and result in E04. |
| I5 — Faithful completion | Rejected partial finish; file lists, hashes and value counts. |
| I6 — Stable terminal | Unchanged outcome after `TOO_LATE`; duplicate idempotency checked separately. |
| I7 — Observation failures | Signal read/write/non-boolean errors; checker ERROR/non-boolean responses and an actual file MISMATCH. |

The suite also covers concurrent duplicates, distinct requests, unit order
and overlap, immutable outcomes, worker failure with unknown effects,
exclusive output creation and path rejection. Reparse-flag rejection uses
a controlled test, not privileged system links.

Presentation tests check default JSON serialization, unchanged saved reports,
dynamic counts, missing data, failed scenarios/saves and error output.
A summary performs no new observation; a supplied checker is not independent
certification.

## Reproduction and limits

The fresh copy used no hardlinks or prior run data. Its imports resolved
inside the copy, tracked bytes matched before and after execution, and both
output modes matched the baseline. `3de166c` closed that verification.
The [recorded failures and fixes](DECISIONS.md) remain part of the history.

The library relies on a cooperative, honest worker. These checks establish
neither arbitrary process or remote cancellation, hostile-process containment,
rollback, general resume, guaranteed latency nor power-loss durability.
[The contract](CONTRACT.md) defines those boundaries.

## Local evidence

Raw logs, byte manifests, earlier failed runs and synthetic results remain
under ignored `.runs/` and `.verification/`. Current presentation
evidence is in `reading_results_20261123`, including
`CLEAN_REPRODUCTION.json`, test logs and both-mode comparisons; earlier
reproduction and reading records remain alongside it.

Those records are excluded from Git and are unnecessary for reproducing the
examples. Historical source material remains private.

Later documentary and attribution edits were checked by byte comparison:
the 53-test result belongs to the tested revision above, not a rerun for those
edits. The repository remains unpublished.

[Try E02](../examples/02_interrupt_copy/README.md) ·
[Contract](CONTRACT.md) · [Origin](ORIGIN.md) · [Main page](../README.md)
