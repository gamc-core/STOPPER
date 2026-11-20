# Candidate verification
20 November 2026 · private review only

## State
| State | Evidence |
| --- | --- |
| IMPLEMENTED | Independent core, five scenarios and caller-owned batch integration. |
| TESTED | 34 distinct tests passed in the original and clean copy. |
| REPRODUCED | Fresh Git copy; identical tracked bytes, isolated import, 5/5 scenarios. |
| PUBLICATION_CANDIDATE | Private candidate; historical summaries await GAMC's publication review. |
| PUBLISHED | No. No remote or package publication. |

Tested implementation revision:
`8cadf809767a4923fec2b397d89fb3ba25051442`.
The closing commit changes documentation only; its executable files are
compared with the hashes retained for this tested revision.

Environment actually tested: Windows 10, build 19045, CPython 3.10.6, 64-bit.
Runtime dependencies: Python standard library only.
Other platforms/interpreters and independent third-party reproduction are
unverified. Installation/wheel building is unverified: the local build
environment lacks wheel; no dependency was downloaded. Source execution is
the verified route. This limit does not prevent the five offline scenarios.

## Reproduce from a new copy
Use the path to your Python interpreter if python is not on PATH.
From a fresh copy of the tracked project:
```text
python -I -S -B tests/run.py
python -I -S -B examples/run.py all
```
Or replace all with E01, E02, E03, E04 or E05.
The runners load only this copy's src. They need neither installation nor
a private environment. All synthetic output stays under this copy's .runs.
Each example saves result.json and prints a relative evidence_directory.

The internal clean-copy verification used a native local Git clone without
hardlinks, imported stopper from that copy, compared all tracked bytes before
and after execution, and preserved stdout, stderr, code hashes and outcomes.
The clone has no remaining remote. It does not contain ignored source-run data.

## Actual scenario outcomes
| Scenario | Observed outcome |
| --- | --- |
| E01 | Wrong-target receipt NOT_RECEIVED; A and B completed; no signal observed. |
| E02 | STOPPED / INTERRUPTED; 2 synthetic files copied, 3 not started; bytes/source hashes checked. |
| E03 | Synthetic modification remained; validation marker absent; no rollback. |
| E04 | COMPLETED / NO_EFFECT; local result existed, delivery suppressed; later TOO_LATE did not rewrite it. |
| E05 | Ordinary arithmetic batch completed 5 values; independent stopped run retained 2 and prevented 3. |

E02 also has an ordinary control using the same copy worker and data shape;
all five files complete without a request. E05 has its own ordinary control.
Worker gates establish ordering; the ten-second waits are failure guards,
not delays used to manufacture when a stop arrives.
File-example teardown checks that no named example worker remains alive.

## Contract coverage
| Invariant | Tests / physical contrast |
| --- | --- |
| I1 request is not effect | Receipt before cooperation; E01 and E04. |
| I2 identity/isolation | Wrong target, separate Events, fixed identity regression, distinct E05 run IDs. |
| I3 no retroactive prevention | Request during active unit; E02; started/prevented sets disjoint. |
| I4 no implicit rollback | E03 retained bytes; E04 retained computed result. |
| I5 faithful partial | Partial finish rejected; E02 names/hashes; E05 result count. |
| I6 late request | Terminal unchanged after TOO_LATE and duplicate receipts. |
| I7 failure is not successful stop | Signal read/write/non-bool failures; checker ERROR/non-bool; actual file MISMATCH. |

Additional checks: duplicate request idempotency (including four concurrent
requests), distinct requests retained, ordered/overlapping units rejected,
immutable outcomes, worker failure retaining unknown active effects, exclusive
destination creation, parent-traversal rejection before mkdir, and rejection
of a reparse flag in a controlled unit test.

Reparse-flag testing did not create actual privileged Windows links or alter
ACLs. The filesystem helpers assume no hostile concurrent path replacement.
A physical checker is supplied code, not an independent certificate. No test
establishes arbitrary process/remote cancellation or universal timing.

## Real findings and corrections
1. The first core suite passed 22 tests. An added identity regression then
   failed: execution_id could be reassigned. The failing test and diagnosis
   were committed before the read-only property fix. The raw local failing
   run remains; its old result is not relabeled.
2. The first fresh copy passed 34 tests and five scenarios but failed exact
   byte comparison on 27 files. System Git autocrlf converted LF to CRLF.
   A repository-local .gitattributes policy corrected checkout representation;
   no global configuration was changed. The corrected fresh-copy run passed
   byte comparison, tests and examples. The first run remains distinct.
3. An optional packaging metadata probe found wheel absent. The unverified
   offline installation command was removed; the no-install route was tested.

## History, privacy and licensing
Git was initialized before implementation, with a new root commit and
incremental contract, implementation, first physical example, negative
regression, fix, remaining scenarios, sanitized documentation, lifecycle review
and checkout correction. No private commits or Git objects were imported.
Local attribution uses a reserved .invalid email; no personal email is needed.

All reachable candidate-history blobs were reviewed for private-path,
credential-marker and personal-email patterns, alongside inspection of the
new files and case summaries. No findings were identified by those checks.
This is a bounded review, not a guarantee that every possible secret pattern
can be detected. Tracked files have no detected symlink/reparse paths.
No private imports, shared Git object store, Git alternates or public remotes
were found. Six focal source-file hashes remained unchanged; no source writes
were performed. That sample is not a complete filesystem audit.

MIT covers the new code, project prose and synthetic data. Historical source
records/conversations are not shipped or relicensed. Case pages are sanitized
new summaries and remain subject to GAMC's review before publication.

## Local evidence retained outside the tracked candidate
Within this project's ignored .verification:
- REPRODUCTION.json: tested revision, file hashes and run results.
- original-final-tests.log and clean-final-tests.log.
- clean-final-examples.jsonl and its stderr log.
- first-reproduction-byte-mismatch.json and the earlier run logs/copy.
- FINAL_AUDIT.json: focused dependency, history, path and provenance checks.
- FINAL_STATE.json: closing HEAD, clean tree and executable-byte comparison.

The ignored .runs/identity_negative_before_fix.txt retains the first failing
identity run. Each physical example's result and synthetic files remain in
the evidence directory reported by its execution. These are local records,
not required private dependencies for reproducing from the tracked files.
Do not include ignored verification copies or runs in an eventual release.

## Residual limits and decision
The core cannot authenticate actors, stop an uncooperative worker, interrupt
inside a unit, undo/resume arbitrary work, control remote providers or promise
crash durability. Worker reports require an appropriate physical check.
No unresolved functional failure remains in the declared tested scope.
Packaging installation, additional platforms and outside-user utility remain
unverified; publication and integration are decisions reserved to GAMC.
