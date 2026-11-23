# Verification

STOPPER's source execution was reproduced in a fresh Git copy on Windows 10
with CPython 3.10.6, 64-bit. The original and clean copy each passed 34 tests;
all five examples passed. Their reports were contrasted with files or data.
The repository has not been published.

## Implementation checked

The tested implementation revision is
`8cadf809767a4923fec2b397d89fb3ba25051442`.
The closing revision `1a1206d` changed documentation only. The 23 November
reading revision also leaves the 13 Python, test and project-metadata files
byte-identical to that tested implementation.

Runtime dependencies are limited to Python's standard library. Package
installation and wheel building remain unverified: the original build
environment lacked wheel, and no dependency was downloaded.
Other platforms, Python versions and independent third-party reproduction
are unverified. Source execution is the checked route.

## Reproduce

From the repository root, using your Python interpreter:

```text
python -I -S -B tests/run.py
python -I -S -B examples/run.py all
```

To begin with one experience, replace `all` with `E02` and follow
[the copy guide](../examples/02_interrupt_copy/README.md). Each example saves
a `result.json` in the new `evidence_directory` it prints.
All synthetic output stays under that checkout's `.runs/`.

The clean reproduction used a local Git clone without hardlinks or copied
run data. Package imports resolved inside that copy. All tracked bytes matched
before and after execution; logs, file hashes and outcomes were retained.

## Observed results

| Scenario | Result |
| --- | --- |
| E01 | `NOT_RECEIVED`; A and B completed without observing a stop signal. |
| E02 | `STOPPED / INTERRUPTED`; two files copied, three never started; bytes and source hashes matched. |
| E03 | The synthetic modification remained; the validation marker was absent. |
| E04 | `COMPLETED / NO_EFFECT`; the result existed while delivery was suppressed. A later `TOO_LATE` request left the outcome unchanged. |
| E05 | An ordinary batch completed five values; a stopped run retained two and prevented three. |

The E02 control uses the same worker without a stop request and completes all
five files. E05 has an ordinary control of its own. Explicit worker/controller
gates establish request order; ten-second waits only detect broken coordination.
File-example teardown checks that no named example worker remains alive.

## Contract coverage

| Invariant | Checks and evidence |
| --- | --- |
| I1 — Request differs from effect | Receipt before cooperation; E01 and E04. |
| I2 — Execution identity | Wrong target, separate default Events, read-only identity regression and distinct E05 IDs. |
| I3 — No retroactive prevention | Request during an active unit; E02; disjoint started/prevented sets. |
| I4 — No implicit rollback | Retained modified bytes in E03 and computed result in E04. |
| I5 — Faithful completion | Rejected partial finish; E02 names/hashes and E05 value counts. |
| I6 — Stable terminal | Outcome unchanged after `TOO_LATE`; duplicate-request idempotency checked separately. |
| I7 — Observation failures | Signal read/write/non-boolean errors; checker ERROR/non-boolean responses and an actual file MISMATCH. |

The suite also covers four concurrent duplicate requests, distinct requests,
ordered and overlapping units, immutable outcomes, worker failure with unknown
active effects, exclusive destination creation and rejection of parent traversal.
Reparse-flag rejection uses a controlled test; no privileged system links or
ACL changes were needed.

The worker still supplies its reports, and the physical checker is supplied
code. These checks do not establish independent certification, hostile-process
containment, arbitrary process cancellation or maximum latency.

## Findings retained

The identity regression failed before its read-only-property correction.
The first clean copy also failed byte identity on 27 files because Git
converted LF to CRLF, even though its tests and examples passed.
A repository-local `.gitattributes` policy fixed checkout representation,
and a new copy passed exact comparison. Both earlier failures remain recorded.
[Development decisions](DECISIONS.md) gives the chronology and commit IDs.

The original review found no matches for its private-path, credential-marker
or personal-email patterns in reachable history. It also found no private
imports, linked tracked paths, Git alternates, shared object store or remotes.
Six focal source-file hashes were unchanged. Those are bounded checks,
not a full source-system audit or a guarantee against every secret pattern.

## Reading revision

23 November 2026: the first-run guide was followed from E02 through its
generated folders and saved result. E01, E03, E04 and E05 were then run using
their documented commands. All five passed, with separate file/data contrasts.

Because the change is editorial, the original 34-test results were retained
rather than represented as a newly executed suite. The 13 executable/test/
metadata files still match the tested hashes. All 303 pre-existing local
evidence files were preserved unchanged.

The linked map uses plain Markdown text and links, so it remains readable
without a diagram renderer. Link targets, heading anchors and the reading
paths were checked locally against the
[GitHub Flavored Markdown syntax](https://github.github.com/gfm/).
No repository content was uploaded for a GitHub-hosted rendering check.
The new changes and reachable history were reviewed for privacy; the earlier
ten commits remain in their original order.

## Local evidence

The ignored `.verification/` retains the original reproduction manifest,
test logs, scenario outputs, first byte-mismatch record, audit and closing
state. The first failing identity log remains in `.runs/`.
The `editorial_20261123` subdirectory holds this reading revision's PRE,
command checks, navigation/privacy report and final state.

These records remain local; they are not dependencies for running from the
tracked files. Existing evidence was not overwritten. An eventual release
must exclude ignored verification copies and runs.

The candidate remains private. MIT covers its new code, prose and synthetic
data; underlying historical records and conversations are not shipped or
relicensed. A human review of the reading experience and publication decision
remain separate from these technical checks.

[First experience](../examples/02_interrupt_copy/README.md) ·
[Contract](CONTRACT.md) · [Origin](ORIGIN.md) · [Main page](../README.md)
