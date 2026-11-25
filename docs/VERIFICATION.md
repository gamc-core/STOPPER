# Verification

Revision `6ebeb69ac145ae1fd8fefe1c1598034dd3abcaf2` passed **62 tests**
in isolated checkouts, through direct paths and an NTFS junction: the existing 53 checks plus nine focal regressions.
All five scenarios ran in JSON and summary modes; saved reports matched
between modes and the earlier baseline byte for byte.

The new tests cover legitimate junction entry, rejection of output junctions,
exclusive creation and signal callback reentry. Windows junction tests use a
native command in disposable synthetic checkouts; other platforms skip those
two checks. Earlier verification remains recorded in Git and local evidence.
Subsequent documentation edits leave the tested Python files unchanged.

Codex assisted the implementation from 20 to 23 November 2026 under GAMC's authorization. A separate
adversarial review conducted with Claude on 23 November 2026 examined behavior, the contract,
concurrency, observable results, reproducibility, path safety and public-history
exposure. Its findings led to targeted fixes; a follow-up review with Claude
independently checked those fixes and the sanitized history later that day.

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

The isolated copies imported their own code and kept tracked bytes unchanged.
The examples also ran through the junction. Checked output junctions and
outside-checkout destinations remained rejected, and existing files were
not overwritten. The [recorded failures and fixes](DECISIONS.md) remain part
of the history.

The library relies on a cooperative, honest worker. These checks establish
neither arbitrary process or remote cancellation, hostile-process containment,
rollback, general resume, guaranteed latency nor power-loss durability.
[The contract](CONTRACT.md) defines those boundaries.

## Local evidence

Raw logs, byte manifests, failed runs and synthetic results remain under
ignored `.runs/` and `.verification/`. The current records are in
`adversarial_resolution_20261123`, including the original failures, corrected
runs, tested-tree identities and both-mode comparisons. Earlier reproduction
and presentation evidence remains alongside them.

Those records are excluded from Git and unnecessary for reproducing the
examples. Historical source material remains private. The repository is
unpublished.

[Try E02](../examples/02_interrupt_copy/README.md) ·
[Contract](CONTRACT.md) · [Origin](ORIGIN.md) · [Main page](../README.md)
