# Development decisions

The Git history records the construction as it happened. The entries below
focus on choices and findings that changed the piece.

## 20 November 2026

### Cooperative work in finite units

The first contract (`3cde351`) chose a conventional `threading.Event`
and a finite, ordered job. Receipts and observed effects stayed separate;
the worker would cooperate before starting another unit.

The initial API (`247a389`) and file examples (`4254000`) made those
boundaries executable. E02's active second file finished before the next
three were prevented. The broader scenarios and independent arithmetic
batch followed in `feaad94`.

### A failed identity check

The initial suites passed 22 and then 26 tests. An added regression exposed
an assignable `execution_id`: the 27-test run had one failure.
The failing test was committed in `8f8c21e` before a read-only property
fixed the binding in `9ad1faa`.

The path review also added rejection of parent traversal and link/reparse
flags. These checks protect the controlled examples; they do not establish
containment against hostile concurrent filesystem changes. The suite then
passed 29 tests and later reached 34.

### Checkout bytes mattered

A fresh Git copy passed 34 tests and all five scenarios but failed byte
identity on 27 files. System Git `core.autocrlf=true` had converted LF
to CRLF. The failure remained recorded.

Repository-local `.gitattributes` fixed checkout representation
(`8cadf80`). A new copy then matched bytes and passed the tests and
examples. `1a1206d` recorded that verification.

A packaging probe found `wheel` unavailable. The unverified offline
installation instruction was removed in `07b0296`; that revision also
checked that example workers had settled. Source execution remained the
verified route.

## 23 November 2026

### Readable examples and optional summaries

Reading revisions `99f531c` and `9ed49ec` connected examples with
their historical cases and first-run steps. I5's wording was clarified:
failure does not confirm completion, even after all units were reported
complete. The behavior did not change.

The existing JSON output had consumers, so `b3ff3eb` added an opt-in
`--summary` in the shared example runner. It reads returned data after
the full report is saved. Core states, synchronization and experiments stayed
unchanged. Nineteen presentation checks brought the suite to 53;
`3de166c` recorded the original and clean-copy results.

A separate comparison initially confused sorted console JSON with saved-file
key order. Comparing the actual files resolved the harness mismatch without
changing the product. Both records were retained.

### Attribution and synthesis

Public attribution and project metadata were aligned to Gonzalo Montero (GAMC)
in `c436710`. Earlier commits were retained. The documentation now separates
origin, decisions and current verification rather than repeating the history
in each place.

[Origin](ORIGIN.md) · [Current verification](VERIFICATION.md) ·
[Main page](../README.md)
