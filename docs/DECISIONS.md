# Development decisions

The repository began before implementation and retains the findings that
changed its construction. Commit IDs below identify that process; the
earlier commits have not been rewritten.

## 20 November 2026

### Scope before code

The first contract (`3cde351`) chose a conventional `threading.Event`
and a finite ordered job. A worker would check between units, while receipts
and observations remained separate. This kept the useful relationship
without importing the private runtime, authority contracts or Git history.

The first implementation (`247a389`) introduced `begin`, `complete`
and `finish`, immutable outcomes and a separate physical-check result.
Its initial suite passed 22 tests.

### First files and a failed identity check

E01 and E02 (`4254000`) put the protocol to work. E02 copied two of five
synthetic files and prevented the next three, checking destination bytes
and unchanged source hashes. The active second unit finished. At that point,
26 tests passed.

An added regression then exposed a real gap: the public `execution_id`
attribute could be reassigned. The 27-test run had one failure.
The failing test was committed first (`8f8c21e`), before a read-only
property fixed the binding (`9ad1faa`).

The same review tightened example paths: parent traversal is rejected before
directory creation, and link/reparse flags are checked. A controlled test
covers flag rejection without creating privileged system links. Private
attribute tampering and hostile filesystem races remain outside the scope.
The suite then passed 29 tests.

### Complete scenarios and limits

The remaining scenarios (`feaad94`) showed a change persisting after stop,
delivery being suppressed while work completed, and reuse in a separate
arithmetic loop. The suite reached 34 tests. Documentation and sanitized
cases followed in `7a4eed2`.

A packaging probe found `wheel` unavailable. An unverified offline pip
instruction was removed; source execution remained the supported reproduction
route. `07b0296` also added checks that example workers had settled.
Installation and wheel building were not validated.

### Clean reproduction and a byte mismatch

The first fresh Git copy passed 34 tests and all five scenarios, but its
byte-identity check failed on 27 files. The copy inherited system Git
`core.autocrlf=true`, converting LF to CRLF. All differences were line
endings; the earlier failure remained recorded.

A repository-local `.gitattributes` policy fixed checkout representation
(`8cadf80`) without changing global Git configuration. A new copy then
matched tracked bytes, passed the same 34 tests and ran all five examples.
Package imports resolved inside that copy. `1a1206d` recorded the close
and its limits.

Git attribution uses a reserved `.invalid` address rather than a personal
email. Code, project prose and synthetic data use MIT; the underlying private
records remain excluded.

## 23 November 2026 — Reading and navigation

The reading revision gives E02 the first-run path, connects examples back to
their source experiences, and places a single linked map in the main page.
Cases use continuous accounts; origin, decisions and verification keep their
separate responsibilities. Internal supervision text and encoding-damaged
headings were removed without rewriting the original commits.

The seven invariants remain. I5's wording now makes clear that a failed
outcome does not confirm completion, even if the worker already reported all
units complete. This clarifies the existing code, including signal failure
at the terminal boundary; it adds no new behavior.

Executable files, tests, license and ignore rules are unchanged. The
[verification record](VERIFICATION.md#reading-revision) identifies the
editorial checks separately from the original test results.

[Origin](ORIGIN.md) · [Verification](VERIFICATION.md) · [Main page](../README.md)
